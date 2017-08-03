Name: snid
Version: 5.0
Release: 3%{?dist}
Summary: Supernova Identification
Group: Sciences/Astronomy
License: GPL
URL: https://people.lam.fr/blondin.stephane/software/%{name}/
Source0: https://people.lam.fr/blondin.stephane/software/%{name}/%{name}-%{version}.tar.gz
Source1: https://people.lam.fr/blondin.stephane/software/%{name}/templates-2.0.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: sed
BuildRequires: pgplot-devel

%description
Supernova Identification.

%prep
%setup -q
%setup -q -D -T -a 1

%build

# patch source to set template directory
sed -i -e 's@INSTALL_DIR/snid-5.0/templates/@%{_datarootdir}/snid/templates-2.0/@g' source/snidmore.f

# increase limits for templates-2.0
sed -i -e 's@MAXPPT = 20000@MAXPPT = 50000@' source/snid.inc
sed -i -e 's@MAXTEMP = 3000@MAXTEMP = 10000@' source/snid.inc

# build the code
make %{?_smp_mflags} FC=gfortran PGLIBS="$(pkg-config --libs pgplot)"

%install
rm -rf %{buildroot}

# install binaries
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 logwave %{buildroot}%{_bindir}/
install -m 755 plotlnw %{buildroot}%{_bindir}/
install -m 755 snid %{buildroot}%{_bindir}/

# install templates
install -m 755 -d %{buildroot}%{_datarootdir}/snid
cp -pr templates %{buildroot}%{_datarootdir}/snid
cp -pr templates-2.0 %{buildroot}%{_datarootdir}/snid

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/logwave
%{_bindir}/plotlnw
%{_bindir}/snid
%{_datarootdir}/snid

%changelog
* Tue Mar 07 2017 Ira W. Snyder <isnyder@lco.global> - 5.0-3
- Use sed to set increased limits for templates-2.0.
* Tue Mar 07 2017 Ira W. Snyder <isnyder@lco.global> - 5.0-2
- Added trailing slash to replacement path in sed command.
* Tue Mar 07 2017 Ira W. Snyder <isnyder@lco.global> - 5.0-1
- Initial creation for supernova team.
