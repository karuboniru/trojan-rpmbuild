Name:		trojan
Version:	1.15.1
Release:	5%{?dist}
Summary:	An unidentifiable mechanism that helps you bypass GFW

Group:		Applications/Internet
License:	GPLv3
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
BuildRequires:	systemd-rpm-macros


%description
An unidentifiable mechanism that helps you bypass GFW.

Trojan features multiple protocols over TLS to avoid both 
active/passive detection and ISP QoS limitations.

Trojan is not a fixed program or protocol. It's an idea, 
an idea that imitating the most common service, 
to an extent that it behaves identically, 
could help you get across the Great FireWall permanently, 
without being identified ever. We are the GreatER Fire; we ship Trojan Horses.


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
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post
%systemd_post trojan.service

%preun
%systemd_preun trojan.service

%postun
%systemd_postun_with_restart trojan.service

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/*
%license LICENSE
%config(noreplace) %{_sysconfdir}/trojan/config.json
%doc %{_mandir}/man1/trojan.1.gz
%doc %{_defaultdocdir}/trojan/*
%{_unitdir}/*


%changelog
* Wed Jun 10 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-5
- Change scripts

* Thu Jun 04 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-4
- rebuilt

* Mon Jun 01 2020 Qiyu Yan <yanqiyu01@gmail.com> - 1.15.1-2
- rebuilt

* Sun Nov 10 2019 Qiyu Yan <yanqiyu01@gmail.com> - 1.13.0-1
- Initial release