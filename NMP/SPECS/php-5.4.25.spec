Name:           php
Version:        5.4.25
Release:        1%{?dist}
Summary:        PHP is a widely-used general-purpose scripting language.

Group:          Development/Languages
License:        PHP License v3.01
URL:            http://www.php.net
Source0:        http://www.php.net/distributions/php-%{version}.tar.gz
#Source1:        %{name}.conf
#Source2:        %{name}.ini
#Source3:        %{name}-fpm.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Vendor:         admin@itnihao.com
Obsoletes:      php

BuildRequires: make
BuildRequires: bzip2 >= 1.0.2-4
BuildRequires: curl-devel >= 7.19.7
BuildRequires: gd-devel >= 2.0.35
BuildRequires: libicu-devel >= 4.0
BuildRequires: libtidy-devel >= 0.9
BuildRequires: libmcrypt-devel >= 2.5.8-2
BuildRequires: glibc-common >= 2.12
#BuildRequires: mhash-devel >= 0.9
BuildRequires: mcrypt >= 2.6
BuildRequires: libtool-ltdl-devel >= 1.5.26-1
BuildRequires: libxml2-devel >= 2.6.32-2
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: openssl-devel >= 0.9.8
BuildRequires: pcre-devel >= 7.8-2
BuildRequires: t1lib-devel >= 5.1.2-1
BuildRequires: zlib-devel >= 1.2.3-3

Requires:      openssl-devel
Requires:      pcre-devel
Requires(pre): shadow-utils
Requires(post): chkconfig

%description
PHP is a widely-used general-purpose scripting language that is especially
suited for Web development and can be embedded into HTML.

%prep
%setup -q -n %{name}-%{version}
%build
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR
%configure  --with-layout=GNU --with-libdir=lib64 --enable-fpm --with-gd --enable-intl --enable-bcmath --enable-mbstring --enable-pcntl --enable-json --enable-soap  --enable-sockets --enable-sqlite-utf8 --enable-zip --enable-shmop --enable-pdo --with-zlib --with-bz2 --with-curl --with-curlwrappers --with-jpeg-dir --with-freetype-dir --with-png-dir --with-iconv --with-xpm-dir --with-zlib-dir --with-gettext --with-pcre-regex --with-mcrypt --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-openssl --with-pdo-mysql=mysqlnd --with-pdo-sqlite --with-tidy=/usr --with-pear=%{_datadir}/php/pear --with-icu-dir=/usr --with-config-file-scan-dir=%{_sysconfdir}/php.d --disable-debug  --disable-ipv6

make %{?_smp_mflags}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/php.d
install -Dp -m0755 sapi/fpm/init.d.php-fpm.in %{buildroot}%{_initrddir}/php-fpm
install -m  644 php.ini-development $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
%{__make} install INSTALL_ROOT="%{buildroot}"
%{__install} -m 755 sapi/fpm/init.d.php-fpm $RPM_BUILD_ROOT%{_initrddir}/php-fpm
%{__cp} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
sed -i "/;date.timezone =/adate.timezone = Asia\/Shanghai" /etc/php.ini
sed -i "s/listen = 127.0.0.1:9000/;listen = 127.0.0.1:9000/g"  /etc/php-fpm.conf
mkdir /var/run/php/
grep "listen = /var/run/php/php-fpm.sock" /etc/php-fpm.conf
[ "$?" != 0 ] && sed -i "/;listen = 127.0.0.1:9000/alisten = /var/run/php/php-fpm.sock\n" /etc/php-fpm.conf
/sbin/chkconfig --add php-fpm
/sbin/chkconfig --level 2345 php-fpm on
/sbin/service php-fpm start

%preun
if [ "$1" = 0 ] ; then
    /sbin/service php-fpm stop > /dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service php-fpm condrestart > /dev/null 2>&1
fi
exit 0

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man1/php*
%{_sysconfdir}/*
%{_sysconfdir}/php.d
%{_datadir}/*
%{_initrddir}/*
%exclude /.channels
%exclude /.depdb
%exclude /.depdblock
%exclude /.filemap
%exclude /.lock
#%config(noreplace) %{_sysconfdir}/php.ini


%changelog
* Sun Feb 23 2014 itnihao         - 5.4.35  <admin@itnihao.com>
- updated to 5.4.25

* Fri Jul  5 2013 Itnihao build   - 5.3.26-1 <admin@itnihao.com>
-  php 5.3.26.1 release

* Fri Jan 25 2013 Itnihao build   - 5.3.21-1 <admin@itnihao.com>

* Wed Dec 21 2011 Mike Willbanks  - 5.3.8-1
- Updated to 5.3.8
* Tue Feb 23 2011 Mike Willbanks  - 5.3.5-1
- Initial Package
