%global _prefix /usr/local
%define  tag     RELEASE.2019-03-27T22-35-21Z
%define  subver  %(echo %{tag} | sed -e 's/[^0-9]//g')

Name:    minio
Version: 0.0.%{subver}
Release: 1
Summary: Minio is an open source object storage server compatible with Amazon S3 APIs
Group:   Development Tools
License: ASL 2.0
Source0: https://dl.minio.io/server/minio/release/linux-amd64/minio.%{tag}
Source1: https://raw.githubusercontent.com/minio/minio-service/master/linux-systemd/distributed/minio.service
Source2: minio
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%description
Minio is an object storage server released under Apache License v2.0. It is compatible with Amazon S3 cloud storage service.
It is best suited for storing unstructured data such as photos, videos, log files, backups and container / VM images.
Size of an object can range from a few KBs to a maximum of 5TB.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir}
%{__install} -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
%{__install} -m 0755 -d %{buildroot}/var/minio
%{__install} -m 0755 -d %{buildroot}/etc/default
%{__install} -m 664 %{SOURCE2} %{buildroot}/etc/default/minio

%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE1} \
    %{buildroot}%{_unitdir}/%{name}.service
%endif

%pre
/usr/bin/getent group minio-user || /usr/sbin/groupadd -r minio-user
/usr/bin/getent passwd minio-user || /usr/sbin/useradd -r -d /var/minio -s /sbin/nologin minio-user

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop %{name}
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
/etc/default/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
