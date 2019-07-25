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
    public static readonly DependencyProperty PdfPathProperty =
        DependencyProperty.Register("PdfPath", typeof(string), typeof(PdfViewer), new PropertyMetadata(null, propertyChangedCallback: OnPdfPathChanged));

    private static void OnPdfPathChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
      var pdfDrawer = (PdfViewer)d;

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
            //var pages = new List<Image>();
            globalPdfViewer = pdfViewer;
            var items = globalPdfViewer.PagesContainer.Items;
            items.Clear();
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
          //items.Add(image);
          globals.pages.Add(image);
        }
            
       }
        changePage(0);

    }

    public static void changePage(int pageNum)
    {
        var items = globalPdfViewer.PagesContainer.Items;

            if (pageNum < globals.pages.Count)
            {
                items.Clear();
                items.Add(globals.pages[pageNum]);
            }
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

        private static BitmapImage ImageToBitmap(RenderTargetBitmap target)
        {
            var bitmapImage = new BitmapImage();
            var bitmapEncoder = new PngBitmapEncoder();
            bitmapEncoder.Frames.Add(BitmapFrame.Create(target));

            using (var stream = new MemoryStream())
            {
                bitmapEncoder.Save(stream);
                stream.Seek(0, SeekOrigin.Begin);

                bitmapImage.BeginInit();
                bitmapImage.CacheOption = BitmapCacheOption.OnLoad;
                bitmapImage.StreamSource = stream;
                bitmapImage.EndInit();
            }
            return bitmapImage;
        }


        public static void TestDraw(int page)
        {
            BitmapImage bmp = globals.pages[page].Source as BitmapImage;
            var items = globalPdfViewer.PagesContainer.Items;

            // bmp is the original BitmapImage
            var target = new RenderTargetBitmap(bmp.PixelWidth, bmp.PixelHeight, bmp.DpiX, bmp.DpiY, PixelFormats.Pbgra32);
            var visual = new DrawingVisual();

            using (var r = visual.RenderOpen())
            {
                //r.DrawImage(bmp, new Rect(0, 0, bmp.Width/2, bmp.Height/2));
                r.DrawLine(new Pen(Brushes.Red, 10.0), new Point(0, 0), new Point(bmp.Width, bmp.Height));
            }

            target.Render(visual);

            

            Application.Current.Dispatcher.BeginInvoke(DispatcherPriority.ApplicationIdle, new Action(() => {
                bmp = ImageToBitmap(target);
                items.Clear();
                items.Add(bmp);
            })).Wait();


        }

        private void changePdf(object sender, RoutedEventArgs e)
        {
            OpenFileDialog choofdlog = new OpenFileDialog();
            choofdlog.Filter = "Pdf Files (*.pdf)|*.pdf";
            //choofdlog.FilterIndex = 1;
            choofdlog.Multiselect = false;
            choofdlog.ShowDialog();
            string sFileName = choofdlog.FileName;
            //changePdf(sFileName);
            //Controls.PdfViewer.changePdf(sFileName);
            //if (DialogResult.HasValue && DialogResult.Value)
            //{

            //Controls.PdfViewer test = new Controls.PdfViewer();
            //test.PdfPath = sFileName;    
            //}
        }

    }
}
