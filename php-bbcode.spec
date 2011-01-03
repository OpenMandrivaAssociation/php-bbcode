%define modname bbcode
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A68_%{modname}.ini

Summary:	BBCode parsing Extension
Name:		php-%{modname}
Version:	1.0.2
Release:	%mkrel 14
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/bbcode
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a quick and efficient BBCode Parsing Library. It provides various tag
types, high speed one pass parsing, callback system, tag position restriction.

It will force closing BBCode tags in the good order, and closing terminating
tags at the end of the string this is in order to ensure HTML Validity in all
case.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

#export CFLAGS="%(echo %optflags | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')"
#export CXXFLAGS="${CFLAGS}"
#export CCFLAGS="${CFLAGS}"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 .libs/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
