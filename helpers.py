
import re
from steam.steamid import SteamID
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats
from flask import Flask, flash, redirect, render_template, request, session, send_file, after_this_request
from models import db, Users, SteamProfiles
from sqlalchemy import and_
from config import steam_api


class ProcessHelper:
    
    steam_user_games =  IPlayerService(steam_api_key=steam_api)
    steam_user_info =  ISteamUser(steam_api_key=steam_api)

    @staticmethod
    def hours_calculator(user_id):

        player_summary = ProcessHelper.steam_user_games.get_recently_played_games(user_id)
        hours = 0

        try:
            for game in player_summary['response']['games']:
                for key in game:
                    hours += game['playtime_2weeks']
                    break

            hours = round(hours / 60)
            status = True

            return status, hours

        except KeyError:
            status = False
            return status, hours

    @staticmethod
    def process_url():
        # Requesting profile link and checking the length

        provided_url = request.form.get("providedurl")
        provided_url_size = len(provided_url)

        correct_input_vanity = re.search('''https://steamcommunity.com/id/''', str(provided_url))
        correct_input_64 = re.search('''https://steamcommunity.com/profiles/''', str(provided_url))

        if ((correct_input_vanity != None) and (provided_url_size >= 32) and (provided_url_size <= 62)) or ((correct_input_64 != None) and (provided_url_size == 53)):
            user_id = SteamID.from_url(provided_url)

            if not user_id:

                if_profile_exists = False

                return render_template('search_profile.html', if_profile_exists=if_profile_exists, provided_url=provided_url) 
            
            status, hours = ProcessHelper.hours_calculator(user_id)

            if user_id != None:

                player_summary = ProcessHelper.steam_user_games.get_recently_played_games(user_id)
                usersummary = ProcessHelper.steam_user_info.get_player_summaries(user_id)['response']['players'][0]

                steam_profile = usersummary['avatarfull']
                user_nickname = usersummary['personaname']
                real_steam_id = str('''http://steamcommunity.com/profiles/''' + usersummary['steamid'])
                if_profile_exists = True

                try:
                    if session['user_id']:

                        record_exists = db.session.query(SteamProfiles).filter(and_(SteamProfiles.steam_profile_id.like(real_steam_id), SteamProfiles.user_id.like(session['user_id']))).first()
                        
                        if record_exists is None:

                            hours2weeks = ProcessHelper.hours_calculator(user_id)
                            hours2weeks = hours2weeks[1]
                            profile_data = SteamProfiles(steam_username=user_nickname, hours_in_2_weeks = hours2weeks, user_id=session['user_id'], steam_profile_pic = steam_profile, steam_profile_id=real_steam_id )
                            db.session.add(profile_data)
                            db.session.commit()

                except KeyError:
                    pass

                return render_template('search_profile.html', hours=hours, status=status, provided_url=provided_url, user_nickname=user_nickname, steam_profile=steam_profile, real_steam_id=real_steam_id,if_profile_exists=if_profile_exists)

            else:
                if_profile_exists = False

                return render_template('search_profile.html', if_profile_exists=if_profile_exists, provided_url=provided_url)

        else:
            if_profile_exists = False

            return render_template('search_profile.html', if_profile_exists=if_profile_exists, provided_url=provided_url)

