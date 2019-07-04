using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Windows.Data.Pdf;
using Windows.Storage;
using Windows.Storage.Streams;
using System.Windows.Forms;

namespace WPF_PDFDocument
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    static class globals
    {
        public static int currentPage = 0;
        public static uint maxPage = 0;
        public static List<Image> pages = new List<Image>();
    }

    public partial class MainWindow : Window
  {
    public MainWindow()
    {
      InitializeComponent();
    }

    private void nextPage(object sender, RoutedEventArgs e)
    {
            if (globals.currentPage < globals.maxPage-1)
            {
                globals.currentPage++;
            } 
            Controls.PdfViewer.changePage(globals.currentPage);
    }

    private void prevPage(object sender, RoutedEventArgs e)
    {
            if (globals.currentPage >= 1)
            {
                globals.currentPage--;
            }
            Controls.PdfViewer.changePage(globals.currentPage);
    }

        private void drawRect(object sender, RoutedEventArgs e)
        {
             Controls.PdfViewer.TestDraw(globals.currentPage);
        }

    

            
    
  }
}
