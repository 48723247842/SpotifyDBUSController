#!/usr/bin/env python3
import dbus
from pprint import pprint

# sudo apt-get install d-feet
# go over to 'Session Bus' Tab and look at org.mpris.MediaPlayer2.spotify

class SpotifyDBusController:

	def __init__( self , options={} ):
		self.options = options
		self.session_bus_name = "org.mpris.MediaPlayer2.Player"
		self.session_bus_object_path = "/org/mpris/MediaPlayer2"
		self.session_bus_interface_name = "org.mpris.MediaPlayer2.spotify"
		self.session_bus_property_interface_name = "org.freedesktop.DBus.Properties"
		self.session_bus = dbus.SessionBus()
		self.session_bus_object = self.session_bus.get_object( self.session_bus_interface_name , self.session_bus_object_path )
		self.session_bus_interface = dbus.Interface( self.session_bus_object , self.session_bus_name )
		self.session_bus_property_interface = dbus.Interface( self.session_bus_object , self.session_bus_property_interface_name )
		self.dbus_type_struct = {
			dbus.String : str,
			dbus.UInt32 : int,
			dbus.Int32 : int,
			dbus.Int16 : int,
			dbus.UInt16 : int,
			dbus.UInt64 : int,
			dbus.Int64 : int,
			dbus.Byte : int,
			dbus.Boolean : bool,
			dbus.ByteArray : str,
			dbus.ObjectPath : str
		}

	def dbus_object_to_python( self , dbus_dictionary ):
		t = type( dbus_dictionary )
		if t in self.dbus_type_struct:
				return self.dbus_type_struct[ t ]( dbus_dictionary )
		if t is dbus.Dictionary:
				return dict( [ ( self.dbus_object_to_python( k ) , self.dbus_object_to_python( v ) ) for k , v in dbus_dictionary.items() ] )
		if t is dbus.Array and dbus_dictionary.signature == "y":
				return "".join( [ chr( b ) for b in dbus_dictionary ] )
		if t is dbus.Array or t is list:
				return [ self.dbus_object_to_python( v ) for v in dbus_dictionary ]
		if t is dbus.Struct or t is tuple:
				return tuple( [ self.dbus_object_to_python( v ) for v in dbus_dictionary ] )
		return dbus_dictionary

	# Methods
	# =================
	def next( self ):
		self.session_bus_interface.Next()

	def previous( self ):
		self.session_bus_interface.Previous()

	def pause( self ):
		self.session_bus_interface.Pause()

	def play( self ):
		self.session_bus_interface.Play()

	def play_pause( self ):
		self.session_bus_interface.PlayPause()

	def stop( self ):
		self.session_bus_interface.Stop()

	def open_uri( self , spotify_uri ):
		self.session_bus_interface.OpenUri( spotify_uri )

	# Might Not Be Seconds ?? Who Knows , why would spotify tell us
	def seek( self , seek_seconds ):
		self.session_bus_interface.Seek( seek_seconds )

	def set_position( self , track_id , position ):
		self.session_bus_interface.SetPosition( track_id , position )

	# Property Getters
	# =================
	def get_can_control( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanControl" )

	def get_can_go_next( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanGoNext" )

	def get_can_go_previous( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanGoPrevious" )

	def get_can_pause( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanPause" )

	def get_can_play( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanPlay" )

	def get_can_seek( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "CanSeek" )

	# Doesn't Seem To Return Actual Spotify Value
	def get_shuffle_status( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "Shuffle" )

	def get_metadata( self ):
		metadata = self.session_bus_property_interface.Get( self.session_bus_name , "Metadata" )
		return self.dbus_object_to_python( metadata )

	def get_maximum_rate( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "MaximumRate" )

	def get_minimum_rate( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "MinimumRate" )

	def get_rate( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "Rate" )

	def get_volume( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "Volume" )

	def get_position( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "Position" )

	def get_loop_status( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "LoopStatus" )

	def get_playback_status( self ):
		return self.session_bus_property_interface.Get( self.session_bus_name , "PlaybackStatus" )

	def get_common_status( self ):
		return {
			"status": self.get_playback_status().lower() ,
			"volume": self.get_volume() ,
			"current_time": self.get_position() ,
			"metadata": self.get_metadata()
		}


	## Property Setters ??
	## ===================
	def set_shuffle_status( shuffle_status=False ):
		#return self.session_bus_property_interface.Set( self.session_bus_name , "Shuffle" , shuffle_status )
		pass

if __name__ == '__main__':
	spotify_dbus_controller = SpotifyDBusController()
	spotify_dbus_controller.play()
	print( spotify_dbus_controller.get_playback_status() )
	'''
	spotify_dbus_controller.stop()
	#spotify_dbus_controller.open_uri( "spotify:playlist:7efbTF6iXgx6AGdGnM7nCU" )
	spotify_dbus_controller.open_uri( "spotify:playlist:7efbTF6iXgx6AGdGnM7nCU" )
	spotify_dbus_controller.play()
	print( spotify_dbus_controller.get_playback_status() )
	print( spotify_dbus_controller.get_metadata() )
	'''
