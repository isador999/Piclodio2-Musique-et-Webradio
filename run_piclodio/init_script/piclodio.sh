#!/bin/sh
### BEGIN INIT INFO
# Provides:          piclodio
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Piclodio init script
# Description:       start piclodio app with Django's server
### END INIT INFO

##-----------------------------------------
## edit this part
##-----------------------------------------

# Name for display
NAME=PICLODIO
# path to the piclodio manage.py
DAEMON=/home/pi/Piclodio2/manage.py
# User who run piclodio
RUN_AS='pi'
# PID file location
PIDFILE=/var/run/$NAME.pid
# Port open
PORT=8000

##-----------------------------------------
## do not touch anything belong this point
##-----------------------------------------

# load lsb lib
. /lib/lsb/init-functions
# If the daemon is not there, then exit.
#test -x $DAEMON || exit 5

case "$1" in
  start)
	# Checked the PID file exists and check the actual status of process
	PID=`ps -ef | grep $DAEMON | grep -v grep | awk '{print $2}'`
	if  [ -n "$PID" ];  then
        	echo "$NAME is running on PID $PID";
	else
		# Start the daemon
		start-stop-daemon  --start --background --quiet --oknodo \
						   --pidfile "$PIDFILE" --make-pidfile \
						   --chuid $RUN_AS \
						   --exec /usr/bin/env -- python \
						   $DAEMON runserver --noreload 0.0.0.0:$PORT
		status=$?
		log_end_msg $status
	fi
	
  ;;
  
  stop)
	log_daemon_msg "Stopping $NAME"
	start-stop-daemon --stop --oknodo --pidfile "$PIDFILE" || echo -n "$NAME not running"
	status=$?
    log_end_msg $status
    rm -f -- $PIDFILE
	
  ;;
 
  restart)
        $0 stop && sleep 2 && $0 start
  ;;
		
  status)
	# Check the status of the process.
	PID=`ps -ef | grep $DAEMON | grep -v grep | awk '{print $2}'`
	if  [ -n "$PID" ];  then
                echo "$NAME running on PID $PID";
        else
 		echo "$NAME is not running"
        fi
  ;;
  
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|status}" >&2
        exit 1
  ;;
esac
 
exit 0
