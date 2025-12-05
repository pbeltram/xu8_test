
#ifndef _MAINWINDOW_H_
#define _MAINWINDOW_H_

#include <QtWidgets/QWidget>
#include <QtCore/QString>

#include <cstddef>
#include <cstdint>
//#include <iostream>
//#include <iomanip>
#include <string>
#include <memory>
#include <typeinfo>
#include <fstream>

#include "ui_mainwindow.h"

#define APP_NAME  "PapiFilePlayer"

//----------------------------------------------------------------------------//
extern bool g_verbose;
extern bool g_print;
extern std::string g_finp;
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
typedef struct Data_StartHeader_tag {
  uint32_t nTestVersion;
  char     szDateTime[128];
  char     szIp[128];
  uint32_t nMtu;
  float    fDeviceTemp;
  uint32_t nNofAtoms;
  uint32_t nAtomSize;
  uint32_t nMetaDataSize;
  uint32_t nDataType;
  uint32_t nDataSize;
  uint32_t nSinglePayload;
  uint32_t nNofPackets;
  uint32_t nFPGARev;
} Data_StartHeader_t;

typedef struct Data_Header_tag {
  uint64_t lDataTimestamp;
  uint32_t nBlockId;
  uint32_t nRawDataSize;
  uint32_t nQueued;
  uint32_t nPacketsMissed;
  uint32_t nCPUsLoads;
  uint32_t nTimesToLeave;
  uint32_t nTimesToResend;
  uint32_t nTail;
} Data_Header_t;
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
class MainWindow : public QWidget, private Ui::MainWindow
{
Q_OBJECT

public: // methods

MainWindow(QWidget *parent = NULL);
~MainWindow();

signals:
void Prev();
void Next();

public Q_SLOTS:

void OnPrev();
void OnNext();

void OnRefreshImage();

protected Q_SLOTS:

protected: // methods

void Init();

void unpack_raw12(const uint8_t* a_raw12, uint8_t* a_raw16, int a_num_pxl);

protected: // data members

QString m_windowTitle;

// NOTE: Captured camera image is hardcoded to ROI=4054x3040 12bpp
const int m_image_width  = 4056;
const int m_image_height = 3040;

std::ifstream m_ifile;
size_t m_file_size;

Data_StartHeader_t m_hdr;
Data_Header_t      m_data_hdr;

size_t m_image_no;
size_t m_nof_images;
size_t m_image_size;

};
//----------------------------------------------------------------------------//

#endif //_MAINWINDOW_H_
