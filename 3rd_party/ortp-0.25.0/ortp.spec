# -*- rpm-spec -*-
#
# ortp -- Real-time Transport Protocol Stack
#
# Default is optimized for Pentium IV but will execute on Pentium II &
# later (i686).

# These 2 lines are here because we can build the RPM for flexisip, in which 
# case we prefix the entire installation so that we don't break compatibility
# with the user's libs.
# To compile with bc prefix, use rpmbuild -ba --with bc [SPEC]
%define 		pkg_name 	%{?_with_bc:bc-ortp}%{!?_with_bc:ortp}
%{?_with_bc: %define 	_prefix		/opt/belledonne-communications}
%define 		srtp 		%{?_without_srtp:0}%{?!_without_srtp:1}

# re-define some directories for older RPMBuild versions which don't. This messes up the doc/ dir
# taken from https://fedoraproject.org/wiki/Packaging:RPMMacros?rd=Packaging/RPMMacros
%define _datarootdir       %{_prefix}/share
%define _datadir           %{_datarootdir}
%define _docdir            %{_datadir}/doc

%ifarch %ix86
%define		ortp_cpu	pentium4
%endif

Summary:	Real-time Transport Protocol Stack
Name:		%pkg_name
Version:	0.25.0
Release:	%(git describe --tags --abbrev=40 | sed -rn 's/^.*-([0-9]+)-g[a-z0-9]{40}$/\1/p' || echo '1')%{?dist}
#to be alined with redhat which changed epoc to 1 for an unknown reason
Epoch:		1
License:	LGPL
Group:		Applications/Communications
URL:		http://linphone.org/ortp/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%ifarch %ix86
BuildArch:	i686
%endif

%description
oRTP is a LGPL licensed C library implementing the RTP protocol
(rfc3550). It is available for most unix clones (primilarly Linux and
HP-UX), and Microsoft Windows.

%package        devel
Summary:        Headers, libraries and docs for the oRTP library
Group:          Development/Libraries
BuildRequires:	doxygen
#to be alined with redhat which changed epoc to 1 for an unknown reason
Epoch:		1
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description    devel
oRTP is a LGPL licensed C library implementing the RTP protocol
(rfc1889). It is available for most unix clones (primilarly Linux and
HP-UX), and Microsoft Windows.

This package contains header files and development libraries needed to
develop programs using the oRTP library.

%ifarch %ix86
%define	ortp_arch_cflags -malign-double -march=i686 -mtune=%{ortp_cpu}
%else
# Must be non-empty
%define ortp_arch_cflags -Wall
%endif
%define ortp_cflags %ortp_arch_cflags -Wall -g -pipe -pthread -O3 -fomit-frame-pointer -fno-schedule-insns -fschedule-insns2 -fno-strict-aliasing

%prep
%setup

%build
%configure \
	--enable-shared \
	--enable-static \
%if !%{srtp}
	--with-srtp=none \
%endif
	--docdir=%{_docdir}

%{__make} -j$RPM_BUILD_NCPUS CFLAGS="%ortp_cflags" CXXFLAGS="%ortp_cflags"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_docdir}/ortp-%{version}/README
%doc %{_docdir}/ortp-%{version}/ChangeLog
%doc %{_docdir}/ortp-%{version}/COPYING
%doc %{_docdir}/ortp-%{version}/AUTHORS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/ortp-%{version}/html/*
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}

%changelog
* Tue Oct 25 2005 Francois-Xavier Kowalski <fix@hp.com>
- Add to oRTP distribution with "make rpm" target
