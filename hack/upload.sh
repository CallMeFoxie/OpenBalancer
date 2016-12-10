#!/bin/sh

[ $# -ne 2 ] && echo "Bad arguments!" && exit 1

TYPE=$1
BUILDFILE=$2
SERVERS=
PACKAGE=
PKGNAME=
case "$TYPE" in
    "controller")
        SERVERS=$(MASTERS)
        PACKAGE=$(MASTERFILE)
        PKGNAME=$(MASTERNAME)
    ;;
    "nodes")
        SERVERS=$(NODES)
        PACKAGE=$(NODEFILE)
        PKGNAME=$(NODENAME)
    ;;
    *)
        echo "Bad type!"
        exit 1
    ;;
esac

for $srv in $(echo $SERVERS | cut -d','); do
    echo "Working on $srv"
    echo "> uploading"
    scp -i $KEYFILE $PACKAGE $USER@$srv:/tmp/package.deb
    echo "> removing old one and cleaning"
    ssh -i $KEYFILE $USER@$srv "dpkg --purge $(PKGNAME) && rm -rf '$(CLEANPATH)'"
    echo "> installing and fixing dependencies"
    ssh -i $KEYFILE $USER@$srv 'dpkg -i /tmp/package.deb && apt-get -f install'
done

echo "Done"