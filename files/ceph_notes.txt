
---
MON
---
ceph-authtool --create-keyring /tmp/ceph.mon.keyring --gen-key -n mon. --cap mon "allow *"
ceph-authtool --create-keyring /etc/ceph/ceph.client.admin.keyring --gen-key -n client.admin --set-uid=0 --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow'

ceph-authtool /tmp/ceph.mon.keyring --import-keyring /etc/ceph/ceph.client.admin.keyring

monmaptool --create --add ip-10-80-60-52 10.80.60.52 --add ip-10-80-60-55 10.80.60.55 --add ip-10-80-60-95 10.80.60.95 --fsid 47fb051f-07ad-4b78-b4b7-b4c8946c468d /tmp/monmap


ceph-mon --mkfs -i ip-10-80-60-52 --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring

touch /var/lib/ceph/mon/ceph-ip-10-80-60-52/done
chown -R ceph:ceph /var/lib/ceph/mon
chown -R ceph:ceph /var/log/ceph
chown -R ceph:ceph /var/run/ceph
chown -R ceph:ceph /etc/ceph/ceph.client.admin.keyring
chown -R ceph:ceph /etc/ceph/ceph.conf
chown -R ceph:ceph /etc/ceph/rbdmap
systemctl enable ceph-mon.target
systemctl enable ceph-mon@ip-10-80-60-52
systemctl start ceph-mon@ip-10-80-60-52

----
MGR
----
ceph auth get-or-create mgr.ip-10-80-60-52 mon 'allow profile mgr' osd 'allow *' mds 'allow *'
mkdir /var/lib/ceph/mgr/ceph-ip-10-80-60-52
cat > /var/lib/ceph/mgr/ceph-ip-10-80-60-52/keyring
systemctl enable ceph-mgr.target
systemctl enable ceph-mgr@ip-10-80-60-52
systemctl start ceph-mgr@ip-10-80-60-52


----
OSD
----
UUID=`uuidgen`
ID=`ceph osd create $UUID`
parted /dev/xvdb mklabel gpt
parted /dev/xvdb mkpart primary 1 100%
<mount fs>
ceph-osd -i 0 --mkfs --mkkey --osd-uuid $UUID
ceph auth add osd.0 osd 'allow *' mon 'allow profile osd' -i /var/lib/ceph/osd/ceph-0/keyring
ceph osd crush add-bucket ip-10-80-60-107 host
ceph osd crush move ip-10-80-60-107 root=default
ceph osd crush add osd.0 1.0 host=ip-10-80-60-107
chown -R ceph:ceph /var/lib/ceph/osd/
chown -R ceph:ceph /var/log/ceph
chown -R ceph:ceph /var/run/ceph/
chown -R ceph:ceph /etc/ceph/
systemctl enable ceph-osd.target
systemctl enable ceph-osd@0
systemctl start ceph-osd@0

----
Config file
----

[global]
fsid = 47fb051f-07ad-4b78-b4b7-b4c8946c468d
mon initial members = ip-10-80-60-52, ip-10-80-60-55, ip-10-80-60-95
mon host = 10.80.60.52, 10.80.60.55, 10.80.60.95

#Enable authentication between hosts within the cluster.
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

public_network = 10.80.60.0/24

osd pool default pg num = 233
osd pool default pgp num = 233
osd journal size = 10000



[client.admin]
	key = AQB+Kphbu5ZkERAA1d9D3/i+5MnxtFEeSsPOuw==
	auid = 0
	caps mds = "allow"
	caps mon = "allow *"
	caps osd = "allow *"
