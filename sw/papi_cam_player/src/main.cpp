
#include <QtCore/QtGlobal>
#include <QtCore/QtDebug>

#include <QtGui/QtGui>

#include <QApplication>

#include <cstddef>
#include <cstdint>
#include <iostream>
#include <string>
#include <memory>
#include <chrono>
#include <tuple>

#ifdef Q_OS_UNIX
#include <sys/resource.h>
#include <execinfo.h>
#include <signal.h>
#include <unistd.h>
#endif

#include <getopt.h>

#include "mainwindow.h"

//----------------------------------------------------------------------------//
bool g_verbose = false;
bool g_print = false;
std::string g_finp("./samples_v1.dat");
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
static void usage(const char *argv0)
{
  std::cout << "Usage: " << argv0 << " [options]" << std::endl;
  std::cout <<
      "-v, --verbose     Print console messages. (Optional, default is off)."
      << std::endl;
  std::cout <<
      "-p, --print       Dump data content if print is enabled. (Optional, default is off)."
      << std::endl;
  std::cout <<
      "-i, --input       Input file name default(\"./input_raw.cf64\")."
      << std::endl;
  std::cout <<
      "-?, --help        Show this help screen."
      << std::endl;
}

static struct option opts[] = {
  /* These options set a flag. */
  { "input",    required_argument, nullptr,    'i' },
  { "out",      required_argument, nullptr,    'o' },
  { "print",    no_argument,       nullptr,    'p' },
  { "verbose",  no_argument,       nullptr,    'v' },
  { "help",     no_argument,       nullptr,    '?' },
  { nullptr,    0,                 nullptr,     0  }
};
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
static std::tuple <uint32_t, uint32_t, uint32_t> parse_int_range(char *sz_int_range)
{
  std::string s(sz_int_range);
  std::string range_delimiter = "..";
  std::string ratio_delimiter = ":";

  size_t pos = 0;
  std::string token;
  uint32_t from_int;
  uint32_t to_int;
  uint32_t ratio_int;

  assert(((pos = s.find(range_delimiter)) != std::string::npos) && ":Parse wrong from range parameter.");
  from_int = atoi(s.substr(0, pos).c_str());
  s.erase(0, pos + range_delimiter.length());
  assert(((pos = s.find(ratio_delimiter)) != std::string::npos) && ":Parse wrong to range parameter.");
  to_int = atoi(s.substr(0, pos).c_str());
  s.erase(0, pos + ratio_delimiter.length());
  assert((s.length() != 0) && ":Parse wrong ratio range parameter.");
  ratio_int = atoi(s.c_str());

  return std::make_tuple(from_int, to_int, ratio_int);
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
static int parse_int(char *sz_num)
{
  size_t sz_len = ::strlen(optarg);
  assert((sz_len > 0) && ":Parse_int sz_num length is 0.");

  int magn_val = 1;
  char *magn_pch = sz_num+sz_len-1;

  if (::isdigit(*magn_pch) == 0) {

    if ('k' == *magn_pch) magn_val = 1024;
    else if ('M' == *magn_pch) magn_val = 1024*1024;
    else {
      assert((false) && ":Parse wrong parameter magnifier.");
    }

    *magn_pch = '\0';
  }
  int ret_int = atoi(sz_num) * magn_val;

  return ret_int;
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
static float parse_float(char *sz_num)
{
  size_t sz_len = ::strlen(optarg);
  assert((sz_len > 0) && ":Parse_float sz_num length is 0.");

  return atof(sz_num);
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
static bool parse(int argc, char *argv[])
{
  // Parse command line arguments.
  int c;
  int option_index = 0;
  while ((c = ::getopt_long(argc, argv, "i:pv?", opts, &option_index)) != -1) {
    switch (c) {
      case '?': {
        usage(argv[0]);
      }
      return false;

      case 'p': {
        g_print = true;
      }
      break;

      case 'v': {
        g_verbose = true;
      }
      break;

      case 'i':
        g_finp = std::string(optarg);
        break;

      break;

      default: {
        std::cout << "Invalid option -" << c << "." << std::endl;
        std::cout << "Run " << argv[0] << " -h for help." << std::endl;
      }
      return false;
    }
  }

  if (optind < argc) {
    std::cout << " Parsing got non-option ARGV-elements: ";
    while (optind < argc) {
      std::cout << argv[optind++] << " ";
    }
    std::cout << std::endl;
    return false;
  }

  return true;
}
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
#ifdef Q_OS_UNIX
static void handle_segmentation_fault(int sig)
{
  printf("\nSegmentation fault\n\n");
  void *array[100];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 100);

  // print out all the frames to stderr
  fprintf(stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd(array, size, STDERR_FILENO);

  exit(EXIT_FAILURE);
}
#endif
//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//
int main(int argc, char *argv[])
{
  if (parse(argc, argv) == false) {
    return -1;
  }

  #ifdef Q_OS_UNIX
  // Set mem alloc limits
  struct rlimit lm_limit;
  lm_limit.rlim_cur = RLIM_INFINITY;
  lm_limit.rlim_max = RLIM_INFINITY;
  if (getrlimit(RLIMIT_MEMLOCK, &lm_limit) < 0) {
    fprintf(stderr, "Warning: setrlimit(RLIMIT_MEMLOCK) returned %d-(%s). Run as sudo.\n", errno, strerror(errno));
  }

  signal(SIGSEGV, handle_segmentation_fault);
  #endif //Q_OS_UNIX

  Q_INIT_RESOURCE(resourcefile);
  setlocale(LC_ALL, ""); // use system's locale

  QApplication app(argc, argv);

  if (g_verbose) {
    qDebug() << "DEBUG: Start application.";
  }
  //QStyleFactory style;
  QFile styleFile(":qtgui/styles/default.css");
  if(styleFile.open(QIODevice::ReadOnly))
  {
    if (g_verbose) {
      qDebug() << "DEBUG: * Got Stylesheet settings file.";
    }
    QTextStream textStream(&styleFile);
    QString styleSheet = textStream.readAll();
    styleFile.close();
    app.setStyleSheet(styleSheet);
  }

  QApplication::setStyle("Fusion");
  #ifdef Q_OS_UNIX
  QFont newFont("Arial", 10, QFont::Normal, false);
  QApplication::setFont(newFont);
  #endif

  MainWindow* w = new MainWindow();
  w->show();

  int status = app.exec();
  delete w;

  if (g_verbose) {
    qDebug() << "DEBUG: Exit with status=" << status;
  }
  return status;
}
//----------------------------------------------------------------------------//
