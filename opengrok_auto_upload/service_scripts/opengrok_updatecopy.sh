#!/bin/bash

# opengrok sync and update automatically
# 04302017 by Roy Wang (gunwoow@qti.qualcomm.com)
# LV.HB.1.1.1
# LV.HB.1.1.2

REPO_DIR_ROOT="/var/opengrok/src"
OPENGROK_LOG="/var/opengrok/log/script.log"
OPENGROK_DIR="/var/opengrok/bin/OpenGrok"
REPO="/usr/bin/repo"

sync_cmd="$REPO sync -c -q --no-tags -j4"
repodirs="LV.HB.1.1.1 LV.HB.1.1.1_rb1 LV.HB.1.1.2 LV.HB.1.1.2_rb1"

function clear_all_modifications
{
	echo "$REPO forall -c 'git checkout -f&&git clean -f -d ./'"
}

function run_repo_sync
{
	repo_prj=$1
	cd ${REPO_DIR_ROOT}/$repodir/

#	echo "$sync_cmd 2>&1" >> $OPENGROK_LOG
	$sync_cmd 2>&1
}

function run_opengrok_update
{
#	echo "$OPENGROK_DIR update" >> $OPENGROK_LOG
	$OPENGROK_DIR update
}

function run_opengrok_index
{
	$OPENGROK_DIR index
}

for repodir in $repodirs
do
	echo "$repodir : repo sync START at `date`" >> $OPENGROK_LOG
	run_repo_sync $repodir
	echo "$repodir : repo sync END at `date`" >> $OPENGROK_LOG
done

echo "opengrok update START at `date`" >> $OPENGROK_LOG
run_opengrok_update
echo "opengrok update END at `date`" >> $OPENGROK_LOG
echo "" >> $OPENGROK_LOG

