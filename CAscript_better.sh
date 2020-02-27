#!/bin/bash

# Certificate Authority script
# Uses: Cert Authority Lab Prep, Cert Auth Lab - Class Activity, Config Apache for HTTPS - Class Activity 1


myIP=$(ip addr | tail -n 4 | head -n 1 | awk -F ' ' '{print$2}');
## Startup

getIP() {
	echo $(ip addr | tail -n 4 | head -n 1 | awk -F ' ' '{print$2}');
}

echo "Enter IPs and Passwords."
echo "1. Use hardcoded IPs and Passwords"
echo "2. Manually enter IPs and Passwords" 
read -p "Selection: " enterInput;
if [ $enterInput -eq 1 ]  
then
	CAip=192.168.7.53;
	WSip=192.168.7.54;
	CApass=2616;
	WSpass=2616;
else
	read -p "Enter the CA IP: " CAip;
	read -p "Enter the Web Server IP: " WSip;
	read -p "Enter the password for CA: " CApass;
	read -p "Enter the password for WS: " WSpass;
fi

COUNTRY="US" ; STATE="Vermont" ; LOCALITY="Burlington" ; ORGNAME="Joyce310" ; ORGUNIT="Joyce310" ; MYNAME="alex" ; EMAIL="" ; CHALL="" ; COMP2="";

setup() {
	testIP=$(getIP)
	#while [ $testIP != $myIP ] ; do echo "Currently in $testIP" ; exit; testIP=$(getIP) ; done;

	the_ip=$1;	
	the_pass=$2;
	sshpass -p $the_pass ssh -o StrictHostKeyChecking=no root@$the_ip << EOF
	
	dhclient;
	echo "Installing packages on $the_ip ..." ; sleep 3;
	sudo yum -y install httpd;
	sudo yum -y install vim;
	sudo systemctl start httpd;
	sudo yum -y install nmap;
	sudo yum -y install sshpass;
	sudo yum -y install mod_ssl;		
	
	echo "Firewall configurations on $the_ip ..." ; sleep 3;
	sudo firewall-cmd --permanent --add-port=443/tcp ;
	sudo firewall-cmd --permanent --add-port=80/tcp ;
	sudo firewall-cmd --permanent --add-port=22/tcp ;
	sudo firewall-cmd --reload;
	sudo systemctl restart firewalld ;
	sudo firewall-cmd --reload;
	sudo systemctl start httpd;	
	
	echo "Exiting SSH to $the_ip ..." ; sleep 1;	
EOF
	sshpass -p $the_pass scp ./index.html root@$the_ip:/var/www/html/index.html ;
	echo "Host $the_ip Done: get IPs, installed httpd, vim, nmap, sshpass. Start httpd.";
	sleep 3;
}

		#setup $CAip $CApass
		#setup $WSip $WSpass


## Cert Auth Lab Prep
#install SSH client and server if not already

install_ssh_ca() {

	the_ip=$1;
	the_pass=$2;
	sshpass -p $the_pass ssh -o StrictHostKeyChecking=no root@$the_ip <<-EOF

	sudo systemctl start sshd || sudo yum install -y openssh-server openssh-clients;
	sudo systemctl start sshd;
	sudo systemctl status sshd;
EOF
	echo "Host $the_ip Done: install/start sshd, open firewall port 22/tcp";
	sleep 3;

}



		#install_ssh_ca $CAip $CApass
		#install_ssh_ca $WSip $WSpass

### Cert Auth Lab Class Activity
## On CA machine (local)
#create CA

create_ca() {
	sshpass -p $CApass ssh -o StrictHostKeyChecking=no root@$CAip <<-EOF
	
	cd /etc/pki/CA;
	touch index.txt;
	echo 1000 > serial;
	#create CA private key
	openssl genrsa -des3 -passout pass:kitty -out private/cakey.pem 2048 -noout;
	openssl rsa -in private/cakey.pem -passin pass:kitty -out private/cakey.pem;
	#create CA cert
cat <<__EOF__ | openssl req -new -x509 -days 365 -key private/cakey.pem -out cacert.pem
$COUNTRY
$STATE
$LOCALITY
$ORGNAME
$ORGUNIT
$MYNAME
$EMAIL
$CHALL
$COMP2
__EOF__

EOF
	
	echo "Host $CApass Done: create CA private key (/etc/pki/CA/private/cakey.pem), create CA cert (/etc/pki/CA/cacert.pem)";
	sleep 3;
}

		#create_ca

## On WS machine (remote)
#generate private key on web server

create_pk_ws() {	
	sshpass -p $WSpass ssh -o StrictHostKeyChecking=no root@$WSip <<-EOF
	cd ~;
		echo "checkpoint 1" ; sleep 3;
#	openssl req -newkey rsa:2048 -keyout websrv.key -out websrv.csr -passout pass:kitty -noout -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGNAME/OU=$ORGUNIT/CN=$MYNAME/emailAddress=alex@orange.fr ";

cat <<__EOF__ | openssl req -newkey rsa:2048 -keyout websrv.key -out websrv.csr -passout pass:kitty 
$COUNTRY
$STATE
$LOCALITY
$ORGNAME
$ORGUNIT
$MYNAME
$EMAIL
$CHALL
$COMP2
__EOF__

	echo "cert request created: " ; cat websrv.csr ; sleep 8;
	#openssl rsa -in private/cakey.pem -passin pass:kitty -out private/cakey.pem;
	echo "checkpoint 2. sending it over" ; sleep 3;
	#scp csr file to CA
EOF
	#sshpass -p $CApass ssh -o StrictHostKeyChecking=no root@$CAip 'exit' ;
	sshpass -p $WSpass scp root@$WSip:~/websrv.csr ~
	sshpass -p $CApass scp ~/websrv.csr root@$CAip:~
#sshpass -p $CApass ssh -o StrictHostKeyChecking=no root@192.168.7.53 'scp root@$CAip:~/websrv.csr ~ ';
	echo "checkpoint 3. should have sent over T_T" ; sleep 3;
#EOF
	echo "Host $WSip Done: created private key, transfered to CA";
	sleep 3;
}
		#create_pk_ws


## On CA machine (local)
#sign cert

sign_cert_ca() {

	sshpass -p $CApass ssh -o StrictHostKeyChecking=no root@$CAip << EOF
	cd ~; ls -la ; sleep 5;
	echo "checkpoint 1... about to sign csr into crt";
	yes | openssl ca -out websrv.crt -infiles ~/websrv.csr;
	
	#sshpass -p $WSpass scp websrv.crt root@$WSip:~ ;
EOF

	sshpass -p $CApass scp root@$CAip:~/websrv.crt ~
	sshpass -p $WSpass scp ~/websrv.crt root@$WSip:~

	echo "Host $CAip Done: created and transfered websrv.crt to WS";
	sleep 3
}
		#sign_cert_ca

### Config Apache for HTTPS

config_apache() {
	sshpass -p $WSpass ssh -o StrictHostKeyChecking=no root@$WSip << EOF
	cp ~/websrv.crt /etc/pki/tls/certs ;
	cp ~/websrv.key /etc/pki/tls/private ;

	sslchangefile="SSLCertificateFile /etc/pki/tls/certs/websrv.crt" ;
	sslorigfile="SSLCertificateFile /etc/pki/tls/certs/localhost.crt" ;
	sslchangekey='SSLCertificateKeyFile /etc/pki/tls/private/websrv.key' ;
	sslorigkey='SSLCertificateKeyFile /etc/pki/tls/private/localhost.key'  ;



	sed -i 's:SSLCertificateFile /etc/pki/tls/certs/localhost.crt:SSLCertificateFile /etc/pki/tls/certs/websrv.crt:' /etc/httpd/conf.d/ssl.conf ;
	sed -i 's:SSLCertificateKeyFile /etc/pki/tls/private/localhost.key:SSLCertificateKeyFile /etc/pki/tls/private/websrv.key:' /etc/httpd/conf.d/ssl.conf ;
	sudo firewall-cmd --reload;
	sudo systemctl start httpd;
EOF

	echo "Host $WSip Done: enabled the SSL cert and key";
	sleep 3;
}
echo "==================================================";
echo "setup" ; sleep 3;
#if ! (setup $CAip $CApass) ; then echo "Failed!!!"; fi
#if ! (setup $WSip $WSpass) ; then echo "Failed!!!"; fi

echo "==================================================";

echo "install ssh for ca" ; sleep 3;
#if ! (install_ssh_ca $CAip $CApass) ; then echo "Failed!!!"; fi
#if ! (install_ssh_ca $WSip $WSpass) ; then echo "Failed!!!"; fi

echo "==================================================";

echo "create CA" ;
#if ! (create_ca) ; then echo "Failed!!!"; fi
echo "==================================================";
echo "create pk for ws" ; 
#if ! (create_pk_ws) ; then echo "Failed!!!"; fi
echo "==================================================";
echo "sign cert as ca" ; 
#if ! (sign_cert_ca) ; then echo "Failed!!!"; fi
echo "==================================================";
echo "config apache" ;
if ! (config_apache) ; then echo "Failed!!!"; fi
echo "==================================================";
echo "Fuck yeah";
