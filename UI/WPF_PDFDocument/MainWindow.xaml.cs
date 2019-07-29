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
        public static int currentMeasure = -1;
        public static List<Image> pages = new List<Image>();
        public static DependencyObject dpObj;
        public static int[,] pointsA = new int[,] { {0, 108, 65, 180, 111 }, { 0, 108, 111, 180, 191 }, { 0, 108, 191, 180, 271 },
                                        {0, 108, 271, 180, 351 }, {0, 108, 351, 180, 431 },{0, 108, 431, 180, 511 },
                                        { 0, 255, 48, 327, 125}, {0, 255, 125, 327, 202 }, {0, 255, 202, 327, 279 },
                                        {0, 255, 279, 327, 356 }, {0, 255, 356, 327, 433 }, {0, 255, 433, 327, 511 },
                                        { 0, 402, 48, 474, 125}, {0, 402, 125, 474, 202 }, {0, 402, 202, 474, 279 },
                                        {0, 402, 279, 474, 356 }, {0, 402, 356, 474, 433 },{0, 402, 433, 474, 511 },
                                        { 0, 549, 48, 621, 125}, {0, 549, 125, 621, 202 }, {0, 549, 202, 621, 279 },
                                        {0, 549, 279, 621, 356 }, {0, 549, 356, 621, 433 },{0, 549, 433, 621, 511 },
                                        { 1, 46, 48, 118, 125}, {1, 46, 125, 118, 202 }, {1, 46, 202, 118, 279 },
                                        {1, 46, 279, 118, 356 }, {1, 46, 356, 118, 433 }, {1, 46, 433, 118, 511 },
                                        { 1, 176, 48, 248, 125}, {1, 176, 125, 248, 202 }, {1, 176, 202, 248, 279 },
                                        {1, 176, 279, 248, 356 }, {1, 176, 356, 248, 433 }, {1, 176, 433, 248, 511 },
                                        { 1, 304, 48, 376, 125}, {1, 304, 125, 376, 202 }, {1, 304, 202, 376, 279 },
                                        {1, 304, 279, 376, 356 }, {1, 304, 356, 376, 433 }, {1, 304, 433, 376, 511 },
                                        { 1, 432, 48, 504, 125}, {1, 432, 125, 504, 202 }, {1, 432, 202, 504, 279 },
                                        {1, 432, 279, 504, 356 }, {1, 432, 356, 504, 433 }, {1, 432, 433, 504, 511 },
                                        { 1, 560, 48, 632, 164}, {1, 560, 164, 632, 280 }, {1, 560, 280, 632, 395 },
                                        {1, 560, 395, 632, 511 },
                                        { 2, 46, 48, 118, 147 }, { 2, 46, 147, 118, 246 }, { 2, 46, 246, 118, 347 },
                                        { 2, 46, 347, 118, 446 }, { 2, 46, 446, 118, 507} };
    }

    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void nextPage(object sender, RoutedEventArgs e)
        {
            if (globals.currentPage < globals.maxPage - 1)
            {
                globals.currentPage++;
            }
            if (globals.currentPage == 0)
            {
                globals.currentMeasure = -1;
            }
            else if (globals.currentPage == 1)
            {
                globals.currentMeasure = 23;
            }
            else if (globals.currentPage == 2)
            {
                globals.currentMeasure = 51;
            }

            Controls.PdfViewer.changePage(globals.currentPage);
        }

        private void prevPage(object sender, RoutedEventArgs e)
        {
            if (globals.currentPage >= 1)
            {
                globals.currentPage--;
            }
            if (globals.currentPage == 0)
            {
                globals.currentMeasure = -1;
            }
            else if (globals.currentPage == 1)
            {
                globals.currentMeasure = 23;
            }
            else if (globals.currentPage == 2)
            {
                globals.currentMeasure = 51;
            }
            Controls.PdfViewer.changePage(globals.currentPage);
        }

        private void nextMeasure(object sender, RoutedEventArgs e)
        {
            int[,] temp = globals.pointsA;
            if (globals.currentMeasure < temp.Length / 5 - 1)
            {
                globals.currentMeasure++;
                globals.currentPage = temp[globals.currentMeasure, 0];
            }
            Controls.PdfViewer.changePage(globals.currentPage);
            Controls.PdfViewer.changeMeasure(temp[globals.currentMeasure, 1], temp[globals.currentMeasure, 2], temp[globals.currentMeasure, 3], temp[globals.currentMeasure, 4]);

        }

        private void prevMeasure(object sender, RoutedEventArgs e)
        {

            int[,] temp = globals.pointsA;
            if (globals.currentMeasure >= 1)
            {
                globals.currentMeasure--;
                globals.currentPage = temp[globals.currentMeasure, 0];
            }
            else
            {
                globals.currentMeasure = 0;
                globals.currentPage = temp[globals.currentMeasure, 0];
            }

            Controls.PdfViewer.changePage(globals.currentPage);
            Controls.PdfViewer.changeMeasure(temp[globals.currentMeasure, 1], temp[globals.currentMeasure, 2], temp[globals.currentMeasure, 3], temp[globals.currentMeasure, 4]);

        }

        private void changePDF(object sender, RoutedEventArgs e)
        {
            Controls.PdfViewer.changePdf();
        }

    }
}
