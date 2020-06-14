Name:       trojan
Version:    1.16.0
Release:    4%{?dist}
Summary:    An unidentifiable mechanism that helps you avoid censorship

#GPLv3+ with opelssl exceptions
License:    GPLv3+
URL:        https://github.com/trojan-gfw/%{name}
Source0:    %{URL}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# signature from release page
Source1:    %{URL}/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
# keyid obtained from upstream auther's GitHub profile
Source2:    https://pgp.key-server.io/0xA1DDD486533B0112

# for build
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    cmake >= 3.7.2
BuildRequires:    boost-devel >= 1.66.0
BuildRequires:    openssl-devel >= 1.1.0
BuildRequires:    mariadb-devel
%if 0%{?fedora} >= 30
BuildRequires:    systemd-rpm-macros
%else
BuildRequires:    systemd
%endif
# for test
BuildRequires:    python3
BuildRequires:    nmap-ncat
BuildRequires:    curl
BuildRequires:    openssl
#for verifying the tarball
BuildRequires:    gnupg2


%description
An unidentifiable mechanism that helps you avoid censorship.

Trojan features multiple protocols over TLS to avoid both 
active/passive detection and ISP QoS limitations.

Trojan is not a fixed program or protocol. It's an idea, 
an idea that imitating the most common service, 
to an extent that it behaves identically, 
could help you get across the Great FireWall permanently, 
without being identified ever.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q
# change cipher list in shipped configuration file&example into PROFILE=SYSTEM
sed -i '/"cipher"/c\        "cipher": "PROFILE=SYSTEM",' examples/*.json-example
sed -i '/"cipher_tls13"/c\        "cipher_tls13": "PROFILE=SYSTEM",' examples/*.json-example


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
%make_build
popd

%install
pushd %{_target_platform}
%make_install
popd

%check
pushd %{_target_platform}
make test
popd

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%{_bindir}/%{name}
%license LICENSE
%dir %{_sysconfdir}/%{name}
%dir %{_pkgdocdir}
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_mandir}/man1/%{name}.1.*
%{_pkgdocdir}/*
%{_unitdir}/%{name}.service


%changelog
* Sun Jun 14 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-4
- Change due to review suggestions
- see: https://bugzilla.redhat.com/show_bug.cgi?id=1846175

* Sat Jun 13 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-3
- Do not patch source, instead, change shipped configuration file

* Sat Jun 13 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-2
- GuideLine: Package must own all directories that it creates

* Fri Jun 12 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-1
- Update to upstream and change due to suggestion by robinlee.sysu@gmail.com

* Fri Jun 12 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-5
- Add CentOS 8 support (CentOS 7 will not be supported)

* Thu Jun 04 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-4
- rebuilt

* Mon Jun 01 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-2
- rebuilt

* Sun Nov 10 2019 Qiyu Yan <yanqiyu01@gmail.com> - 1.13.0-1
- Initial release
