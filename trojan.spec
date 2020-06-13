Name:		trojan
Version:	1.16.0
Release:	2%{?dist}
Summary:	An unidentifiable mechanism that helps you avoid censorship

License:	GPLv3+
URL:		https://github.com/trojan-gfw/trojan
Source0:	https://codeload.github.com/trojan-gfw/trojan/tar.gz/v%{version}
Patch0:		trojan-ssl_cipher_list.patch

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	mariadb-devel
%if 0%{?fedora} >= 30
BuildRequires:	systemd-rpm-macros
%else
BuildRequires:	systemd
%endif

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
%setup -q
%patch0 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post
%systemd_post trojan.service

%preun
%systemd_preun trojan.service

%postun
%systemd_postun_with_restart trojan.service

%files
%{_bindir}/*
%license LICENSE
%dir %{_sysconfdir}/trojan
%dir %{_pkgdocdir}
%config(noreplace) %{_sysconfdir}/trojan/config.json
%{_mandir}/man1/trojan.1.*
%{_pkgdocdir}/*
%{_unitdir}/*


%changelog
* Sat Jun 13 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-2
- GuideLine: Package must own all directories that it creates

* Fri Jun 12 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.16.0-1
- Update to upstream and change due to suggestion by robinlee.sysu@gmail.com

* Fri Jun 12 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-4
- Add CentOS 8 support (CentOS 7 will not be supported)

* Wed Jun 10 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-5
- Change scripts

* Thu Jun 04 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-4
- rebuilt

* Mon Jun 01 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-2
- rebuilt

* Sun Nov 10 2019 Qiyu Yan <yanqiyu01@gmail.com> - 1.13.0-1
- Initial release
