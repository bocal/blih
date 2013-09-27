#
# spec file for package 
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           blih
Version:        1
Release:        3
License:        Bocal
Summary:        Bocal Lightweight Interface for Humans
Url:    http://repo.epitech.eu/opensuse/
Group:  Basic
BuildRoot:      %{_topdir}/BUILDROOT/

%description
Bocal Lightweight Interface for Humans

%build
cd %{_sourcedir};

%install
rm -fR $RPM_BUILD_ROOT;
mkdir -p $RPM_BUILD_ROOT/usr/bin;
cd %{_sourcedir}
mv blih $RPM_BUILD_ROOT/usr/bin;

%files
%attr(755,root,root)
/usr/bin/blih
