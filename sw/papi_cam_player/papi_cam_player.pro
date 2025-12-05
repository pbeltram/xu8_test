#To make Makefile run: qmake -o Makefile papi_cam_player.pro

QT += \
    core \
    gui \
    widgets \

TARGET = papi_cam_player
TEMPLATE = app

CONFIG += \
    qt \
    warn_on \
    thread \
    debug

DEPENDPATH  += ./src
INCLUDEPATH += ./src

CONFIG(debug, debug|release) {
    DESTDIR     = ./Debug
    OBJECTS_DIR = ./Debug/obj
    MOC_DIR     = ./Debug/moc
    RCC_DIR     = ./Debug/rcc
    UI_DIR      = ./Debug/ui
} else {
    DESTDIR     = ./Release
    OBJECTS_DIR = ./Release/obj
    MOC_DIR     = ./Release/moc
    RCC_DIR     = ./Release/rcc
    UI_DIR      = ./Release/ui
}

!win32:QMAKE_CXXFLAGS += \
    -std=c++11 \
    -Wno-unused-function \
    -Wno-sign-compare \
    -pthread \
    -fvisibility=hidden \
    -fexceptions \
    -fno-check-new \
    -fno-common \
    -fPIC \
    -msse2 \

DEFINES += "_CRT_SECURE_NO_WARNINGS"
DEFINES += "_CRT_SECURE_NO_DEPRECATE"

RESOURCES   += \
    ./src/resourcefile.qrc \

FORMS       += \
    src/ui/mainwindow.ui

HEADERS     += \
    ./src/mainwindow.h \

SOURCES     += \
    ./src/mainwindow.cpp \
    ./src/main.cpp \


extraclean.commands = find . -type f -name \"*.lst\" -exec rm -v {} \\;
clean.depends = extraclean
QMAKE_EXTRA_TARGETS += clean extraclean
