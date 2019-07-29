using System;
using System.Collections.Generic;
using System.IO;
using System.Drawing;
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
using System.Windows.Threading;
using Windows.Data.Pdf;
using Windows.Storage;
using Windows.Storage.Streams;
using OpenFileDialog = System.Windows.Forms.OpenFileDialog;


namespace WPF_PDFDocument.Controls
{
  /// <summary>
  /// Interaction logic for PdfViewer.xaml
  /// </summary>
  public partial class PdfViewer : UserControl
  {

        #region Bindable Properties
    public static PdfViewer globalPdfViewer;

    public string PdfPath
    {
      get { return (string)GetValue(PdfPathProperty); }
      set { SetValue(PdfPathProperty, value); }
    }

    // Using a DependencyProperty as the backing store for PdfPath.  This enables animation, styling, binding, etc...
    public static DependencyProperty PdfPathProperty =
        DependencyProperty.Register("PdfPath", typeof(string), typeof(PdfViewer), new PropertyMetadata(null, propertyChangedCallback: OnPdfPathChanged));

    private static void OnPdfPathChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
      if (globals.dpObj == null)
        {
            globals.dpObj = d;
        }
                
      var pdfDrawer = (PdfViewer)d;
            globals.pages.Clear();
            globals.currentMeasure = -1;
            globals.currentPage = 0;

      if (!string.IsNullOrEmpty(pdfDrawer.PdfPath))
      {
        //making sure it's an absolute path
        var path = System.IO.Path.GetFullPath(pdfDrawer.PdfPath);

        StorageFile.GetFileFromPathAsync(path).AsTask()
          //load pdf document on background thread
          .ContinueWith(t => PdfDocument.LoadFromFileAsync(t.Result).AsTask()).Unwrap()
          //display on UI Thread
          .ContinueWith(t2 => PdfToImages(pdfDrawer, t2.Result), TaskScheduler.FromCurrentSynchronizationContext());
      }

    }
   

    #endregion


    public PdfViewer()
    {
      InitializeComponent();
    }

    private async static Task PdfToImages(PdfViewer pdfViewer, PdfDocument pdfDoc)
    {
            
            globalPdfViewer = pdfViewer;
            
            globals.maxPage = pdfDoc.PageCount;
            
      if (pdfDoc == null) return;

      for (uint i = 0; i < pdfDoc.PageCount; i++)
      {
        using (var page = pdfDoc.GetPage(i))
        {
          var bitmap = await PageToBitmapAsync(page);
          var image = new Image
          {
            Source = bitmap,
            HorizontalAlignment = HorizontalAlignment.Center,
            Margin = new Thickness(0, 4, 0, 4),
            MaxWidth = 800,
            MaxHeight = 700
          };
          globals.pages.Add(image);
        }
            
       }
        changePage(0);

    }

    public static void changePage(int pageNum)
    {
        var items = globalPdfViewer.PagesContainer.Items;
        var highlight = globalPdfViewer.hightlight;
        //var bitmap = globals.pages[pageNum].Source;

        if (pageNum < globals.pages.Count)
        {
                
                
            items.Clear();
            items.Add(globals.pages[pageNum]);
            if (globalPdfViewer.hightlight.Children.Count >= 2)
            {
                globalPdfViewer.hightlight.Children.RemoveAt(globalPdfViewer.hightlight.Children.Count - 1);
            }
                
        }
    }

    public static void changeMeasure(int top, int left, int bottom, int right)
    {
        changeHighlight(top, left, bottom, right);
    }

    public static void changeHighlight(double top, double left, double bottom, double right)
    {
        Rectangle r = new Rectangle();
            

        if (globalPdfViewer.hightlight.Children.Count >= 2)
        {
            globalPdfViewer.hightlight.Children.RemoveAt(globalPdfViewer.hightlight.Children.Count - 1);
        }

        SolidColorBrush red = new SolidColorBrush();
        red.Color = Color.FromRgb(255, 0, 0);
        red.Opacity = 0.25;
        r.Width = right - left;
        r.Height = bottom - top;
        r.Fill = red;
        double tempHeight = globals.pages[0].MaxHeight;
        double tempWidth = globals.pages[0].MaxWidth;

        Canvas.SetLeft(r, left);
        Canvas.SetTop(r, top);

        globalPdfViewer.hightlight.Children.Add(r);
    }

    private static async Task<BitmapImage> PageToBitmapAsync(PdfPage page)
    {
      BitmapImage image = new BitmapImage();

      using (var stream = new InMemoryRandomAccessStream())
      {
        await page.RenderToStreamAsync(stream);

        image.BeginInit();
        image.CacheOption = BitmapCacheOption.OnLoad;
        image.StreamSource = stream.AsStream();
        image.EndInit();
      }

      return image;
    }

    public static void changePdf()
    {
        string filePath;
        OpenFileDialog dialog = new OpenFileDialog();
        dialog.Filter = "pdf files (*.pdf)|*.pdf";
        dialog.ShowDialog();
        filePath = dialog.FileName;

        globals.dpObj.SetValue(PdfPathProperty, filePath);
    }

    }
}
