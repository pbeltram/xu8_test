
#include <QtCore/QtGlobal>
#include <QtCore/QtDebug>

#include <QtGui/QtGui>

#include "mainwindow.h"

//----------------------------------------------------------------------------//
MainWindow::MainWindow(QWidget *parent) : QWidget(parent)
{
  if (g_verbose) {
    qDebug() << "DEBUG: Constructor of MainWindow called.";
  }

  setupUi(this);

  m_windowTitle = APP_NAME;

  Init();

  m_ifile.open(g_finp.c_str(), std::ios::binary | std::ios::ate);
  Q_ASSERT_X((m_ifile.is_open() == true), "MainWindow", "File not open.");
  m_file_size = m_ifile.tellg();
  Q_ASSERT_X((m_file_size > sizeof(Data_StartHeader_t)), "MainWindow", "File size wrong.");

  m_ifile.seekg(0);
  m_ifile.read(reinterpret_cast<char *>(&m_hdr), sizeof(Data_StartHeader_t));
  Q_ASSERT_X((m_ifile.fail() == false), "MainWindow", "Read of StartHeader failed.");

  m_image_size = m_hdr.nDataSize - m_hdr.nMetaDataSize;
  size_t image_size_1 = m_hdr.nAtomSize*m_hdr.nNofAtoms;
  Q_ASSERT_X((m_image_size == image_size_1), "MainWindow", "Image size check failed.");

  m_nof_images = (m_file_size - sizeof(Data_StartHeader_t)) / (sizeof(Data_Header_t)+m_image_size);
  size_t images_size = m_nof_images*(sizeof(Data_Header_t)+m_image_size);
  Q_ASSERT_X(((images_size+sizeof(Data_StartHeader_t)) == m_file_size), "MainWindow", "Bad data file size.");

  m_nofImages->setText(QString("%1").arg(m_nof_images));

  m_image_no = 0;
  OnRefreshImage();
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
void MainWindow::Init()
{
  setWindowTitle(m_windowTitle);

  connect(m_prevBtn, SIGNAL(clicked()), this, SLOT(OnPrev()));
  connect(m_nextBtn, SIGNAL(clicked()), this, SLOT(OnNext()));

  connect(this, SIGNAL(Prev()), this, SLOT(OnRefreshImage()));
  connect(this, SIGNAL(Next()), this, SLOT(OnRefreshImage()));
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
MainWindow::~MainWindow()
{
  if (g_verbose) {
    qDebug() << "DEBUG: Destructor of MainWindow called.";
  }

  m_ifile.close();

  disconnect(m_prevBtn, SIGNAL(clicked()), this, SLOT(OnPrev()));
  disconnect(m_nextBtn, SIGNAL(clicked()), this, SLOT(OnNext()));

  disconnect(this, SIGNAL(Next()), this, SLOT(OnRefreshImage()));
  disconnect(this, SIGNAL(Prev()), this, SLOT(OnRefreshImage()));

  if (g_verbose) {
    qDebug() << "DEBUG: Destructor of MainWindow done.";
  }
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
void MainWindow::OnPrev()
{
  if (m_image_no == 0) m_image_no = m_nof_images-1;
  else m_image_no -= 1;

  emit Prev();
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
void MainWindow::OnNext()
{
  m_image_no = (m_image_no + 1) % m_nof_images;

  emit Next();
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
void MainWindow::OnRefreshImage()
{
  std::streamoff offset = m_image_no*(sizeof(Data_Header_t)+m_image_size)+sizeof(Data_StartHeader_t);

  m_imageNo->setText(QString("%1").arg(m_image_no+1));

  if (g_verbose) {
    qDebug() << "DEBUG: OnRefreshImage:"
        << " image_no=" << m_image_no
        << " offset=" << offset;
  }

  m_ifile.seekg(offset);
  Q_ASSERT_X((m_ifile.fail() == false), "OnRefreshImage", "File seek position failed.");

  m_ifile.read(reinterpret_cast<char *>(&m_data_hdr), sizeof(Data_Header_t));
  Q_ASSERT_X((m_ifile.fail() == false), "OnRefreshImage", "Read of DataHeader failed.");

  QByteArray raw12(m_image_size, 0);
  m_ifile.read(raw12.data(), m_image_size);
  Q_ASSERT_X((m_ifile.fail() == false), "OnRefreshImage", "File image data read failed.");

  size_t num_pxls = m_image_width * m_image_height;
  QByteArray raw16(num_pxls*sizeof(quint16), 0);

  Q_ASSERT_X((((m_data_hdr.nRawDataSize*2)/3) == num_pxls), "OnRefreshImage", "Pixels size and nRawdataSize mismatch.");

  const uint8_t* image_data12 = reinterpret_cast<const uint8_t *>(raw12.constData());
  uint8_t* image_data16 = reinterpret_cast<uint8_t *>(raw16.data());

  unpack_raw12(image_data12, image_data16, num_pxls);

  // Display in Grayscale16 format.
  QImage rawImage(image_data16, m_image_width, m_image_height, m_image_width * sizeof(quint16), QImage::Format_Grayscale16);

  QPixmap pixmap = QPixmap::fromImage(rawImage);
  m_imageLabel->setPixmap(pixmap);
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
void MainWindow::unpack_raw12(const uint8_t* a_raw12, uint8_t* a_raw16, int a_num_pxl)
{
  const uchar* in_data = a_raw12;
  quint16* out_data = reinterpret_cast<quint16*>(a_raw16);

  // Unpack P0|P1 from 24bits.
  //P0​=((Byte1 & 0x0f) << 8) | Byte0
  //P1​=(Byte2 << 4) | ((Byte1 & 0xf0) >> 4)

  //Maximize contrast and brightness to 16bit
  //P0 = P0 << 4;
  //P1 = P1 << 4;
  for (size_t i = 0; i < a_num_pxl; i += 2) {
    size_t bidx = (i / 2) * 3;
    out_data[i]   = (quint16)(((in_data[bidx + 1] & 0x0f) << 8) | in_data[bidx]) << 4;
    out_data[i+1] = (quint16)((in_data[bidx + 2] << 4) | (in_data[bidx + 1] >> 4)) << 4;
  }
}
//----------------------------------------------------------------------------//
