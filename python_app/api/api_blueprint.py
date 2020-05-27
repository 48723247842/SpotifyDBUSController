from sanic import Blueprint
from sanic.response import json
from sanic import response

import time
import redis
from SpotifyDBusController import SpotifyDBusController

def decode_spotify_uri_string( spotify_uri_string ):
	decoded = spotify_uri_string.split( ":" )
	if len( decoded ) < 2:
		return False
	if len( decoded ) == 2:
		if decoded[ 0 ] != "album" or decoded[ 0 ] != "playlist" or decoded[ 0 ] != "track":
			return False
		else:
			decoded.insert( 0 , "spotify" )
	decoded = ":".join( decoded )
	return decoded


api_blueprint = Blueprint( 'api_blueprint' , url_prefix='/api' )

@api_blueprint.route( '/' )
def commands_root( request ):
	return response.text( "you are at the /api url\n" )

# @api_blueprint.route( "/reopen-spotify" , methods=[ "GET" ] )
# def next( request ):
# 	result = { "message": "failed" , "status": None , "metadata": None }
# 	try:

# 		time.sleep( .5 )
# 		result["message"] = "success"
# 	except Exception as e:
# 		print( e )
# 		result["error"] = str( e )
# 	return json( result )


@api_blueprint.route( "/next" , methods=[ "GET" ] )
def next( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.next()
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/previous" , methods=[ "GET" ] )
def previous( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.previous()
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/pause" , methods=[ "GET" ] )
def pause( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.pause()
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/play-pause" , methods=[ "GET" ] )
def play_pause( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.play_pause()
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/stop" , methods=[ "GET" ] )
def stop( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.stop()
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/play" , methods=[ "GET" ] )
def play_uri( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		uri = request.args.get( "uri" )
		if uri == None:
			raise Exception( "no uri in request.args" )
		spotify_uri = decode_spotify_uri_string( uri )
		print( spotify_uri )
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.open_uri( spotify_uri )
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/seek/<seconds>" , methods=[ "GET" ] )
def seek( request , seconds ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.seek( seconds )
		time.sleep( .5 )
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

# Nees /set/position?track_id=asdf&position=2134
@api_blueprint.route( "/set/position" , methods=[ "GET" ] )
def set_position( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		track_id = request.args.get( "track_id" )
		if track_id == None:
			raise Exception( "no track_id in request.args" )
		if position == None:
			raise Exception( "no position in request.args" )

		spotify_dbus_controller = SpotifyDBusController()
		spotify_dbus_controller.set_position( track_id , position )
		time.sleep( .5 )
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["message"] = "success"
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/control" , methods=[ "GET" ] )
def get_can_control( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_control = spotify_dbus_controller.get_can_control()
		result["message"] = "success"
		result["can_control"] = can_control
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/go/next" , methods=[ "GET" ] )
def get_can_go_next( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_go_next = spotify_dbus_controller.get_can_go_next()
		result["message"] = "success"
		result["can_go_next"] = can_go_next
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/go/previous" , methods=[ "GET" ] )
def get_can_go_previous( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_go_previous = spotify_dbus_controller.get_can_go_previous()
		result["message"] = "success"
		result["can_go_previous"] = can_go_previous
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/pause" , methods=[ "GET" ] )
def get_can_pause( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_pause = spotify_dbus_controller.get_can_pause()
		result["message"] = "success"
		result["can_pause"] = can_pause
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/play" , methods=[ "GET" ] )
def get_can_play( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_play = spotify_dbus_controller.get_can_play()
		result["message"] = "success"
		result["can_play"] = can_play
		result["status"] = spotify_dbus_controller.get_shuffle_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/can/seek" , methods=[ "GET" ] )
def get_can_seek( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		can_seek = spotify_dbus_controller.get_can_seek()
		result["message"] = "success"
		result["can_seek"] = can_seek
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/shuffle/status" , methods=[ "GET" ] )
def get_shuffle_status( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		shuffle_status = spotify_dbus_controller.get_shuffle_status()
		result["message"] = "success"
		result["shuffle_status"] = shuffle_status
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/metadata" , methods=[ "GET" ] )
def get_metadata( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		metadata = spotify_dbus_controller.get_metadata()
		result["message"] = "success"
		result["metadata"] = metadata
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/maximum/rate" , methods=[ "GET" ] )
def get_maximum_rate( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		maximum_rate = spotify_dbus_controller.get_maximum_rate()
		result["message"] = "success"
		result["maximum_rate"] = maximum_rate
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/minimum/rate" , methods=[ "GET" ] )
def get_maximum_rate( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		minimum_rate = spotify_dbus_controller.get_minimum_rate()
		result["message"] = "success"
		result["minimum_rate"] = minimum_rate
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/rate" , methods=[ "GET" ] )
def get_rate( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		rate = spotify_dbus_controller.get_rate()
		result["message"] = "success"
		result["rate"] = rate
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/volume" , methods=[ "GET" ] )
def get_volume( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		volume = spotify_dbus_controller.get_volume()
		result["message"] = "success"
		result["volume"] = volume
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/position" , methods=[ "GET" ] )
def get_position( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		position = spotify_dbus_controller.get_position()
		result["message"] = "success"
		result["position"] = position
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/loop/status" , methods=[ "GET" ] )
def get_loop_status( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		loop_status = spotify_dbus_controller.get_loop_status()
		result["message"] = "success"
		result["loop_status"] = loop_status
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

@api_blueprint.route( "/get/playback/status" , methods=[ "GET" ] )
def get_playback_status( request ):
	result = { "message": "failed" , "status": None , "metadata": None }
	try:
		spotify_dbus_controller = SpotifyDBusController()
		result["message"] = "success"
		result["status"] = spotify_dbus_controller.get_playback_status()
		result["metadata"] = spotify_dbus_controller.get_metadata()
	except Exception as e:
		print( e )
		result["error"] = str( e )
	return json( result )

# @api_blueprint.route( "/set/shuffle/status/<status>" , methods=[ "GET" ] )
# def get_loop_status( request ):
# 	result = { "message": "failed" , "status": None , "metadata": None }
# 	try:
# 		spotify_dbus_controller = SpotifyDBusController()
# 		spotify_dbus_controller.set_shuffle_status( status )
# 		result["status"] = spotify_dbus_controller.get_playback_status()
# 		result["metadata"] = spotify_dbus_controller.get_metadata()
# 	except Exception as e:
# 		print( e )
# 		result["error"] = str( e )
# 	return json( result )