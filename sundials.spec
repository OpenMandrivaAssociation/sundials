%define	major 5
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d

%bcond_with	cuda
%bcond_without	atlas
%bcond_without	fortran
%bcond_with	lapack
%bcond_without	pthread

# Can't mix clang (C/C++) and gcc (fortran) when using LTO
%global _disable_lto 1

Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Name:		sundials
Version:	6.2.0
Release:	1
License:	BSD
Group:		Sciences/Computer science
URL:		https://computation.llnl.gov/projects/%{name}
Source0:	https://github.com/LLNL/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gcc-gfortran
%if %{with atlas}
BuildRequires:	libatlas-devel
%endif
%if %{with lapack}
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
%endif
BuildRequires:	libgomp-devel
BuildRequires:	openmpi-devel
%ifarch %{ix86} x86_64
BuildRequires:	quadmath-devel
%endif
BuildRequires:	suitesparse-devel

%description
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Group:		System/Libraries

%description -n %{libname}
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

%files -n %{libname}
%{_libdir}/*.so.*

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for the SUNDIALS libraries
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name}.

%files -n %{develname}
%license LICENSE
%doc README.md
%{_includedir}/*/*.h
%if %{with fortran}
%{_includedir}/*.mod
%endif
%{_includedir}/%{name}/NOTICE
%{_libdir}/lib%{name}_*.so
%{_libdir}/cmake/%{name}/*.cmake
%{_datadir}/%{name}/examples

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
	-DBUILD_FORTRAN77_INTERFACE:BOOL=OFF \
	-DBUILD_FORTRAN_MODULE_INTERFACE:BOOL=%{?with_fortran:ON}%{!?with_fortran:OFF} \
	-DFortran_INSTALL_MODDIR:PATH=%{_includedir} \
	-DENABLE_MPI:BOOL=OFF \
	-DENABLE_OPENMP:BOOL=ON \
	-DENABLE_PTHREAD:BOOL=%{?with_pthread:ON}%{!?with_pthread:OFF} \
	-DENABLE_CUDA:BOOL=%{?with_cuda:ON}%{!?with_cuda:OFF} \
%if %{with lapack}
	-DENABLE_LAPACK:BOOL=%{?with_lapack:ON}%{!?with_lapack:OFF} \
%endif
%if %{with atlas}
	-DENABLE_LAPACK:BOOL=%{?with_atlas:ON}%{!?with_atlas:OFF} \
	-DLAPACK_LIBRARIES:STRING="-L%{_libdir}/atlas -ltatlas" \
%endif
	-DENABLE_KLU:BOOL=ON \
	-DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
	-DKLU_LIBRARY_DIR:PATH=%{_libdir} \
	-DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/examples \
	-DEXAMPLES_ENABLE_CXX:BOOL=ON \
	-DCMAKE_C_STANDARD=17 \
	%{nil}
cd ..
%make_build -C build

%install
%make_install -C build

rm %{buildroot}%{_includedir}/sundials/LICENSE
