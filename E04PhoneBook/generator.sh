#!/bin/sh

fidl=$1
echo $fidl
/home/clivelau/Workspace/TBox-2.0/apps_proc/autolink/tools/commonapi-generator/commonapi-generator-linux-x86 -sk $fidl -d src-gen/core
/home/clivelau/Workspace/TBox-2.0/apps_proc/autolink/tools/commonapi_dbus_generator/commonapi-dbus-generator-linux-x86 $fidl -d src-gen/dbus

