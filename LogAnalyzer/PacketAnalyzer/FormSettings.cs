using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Text.RegularExpressions;

namespace CustomWireshark
{
    public partial class FormSettings : Form
    {
        public FormSettings()
        {
            InitializeComponent();
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.OK;
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
        }

        public SystemSettings settings
        {
            get
            {
                SystemSettings s = new SystemSettings();
                s.enableSaveLog = chkEnableLog.Checked;
                s.savePathLog = lbLogSavePath.Text;
                s.logLevel = cbLogLevel.SelectedItem.ToString();
                s.savePathDump = lbDumpSavePath.Text;
                s.fileNameDump = tbxFileName.Text;

                return s;
            }
            set
            {
                chkEnableLog.Checked = value.enableSaveLog;
                lbLogSavePath.Text = value.savePathLog;
                cbLogLevel.SelectedItem = value.logLevel;
                lbDumpSavePath.Text = value.savePathDump;
                tbxFileName.Text = value.fileNameDump;
            }
        }

        private void btnLogPath_Click(object sender, EventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    lbLogSavePath.Text = dlg.SelectedPath;
                }
            }
            catch(Exception exc)
            {

            }
            finally
            {

            }
        }

        private void btnDumpPath_Click(object sender, EventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    lbDumpSavePath.Text = dlg.SelectedPath;
                }
            }
            catch (Exception exc)
            {

            }
            finally
            {

            }
        }

        private void tbxFileName_TextChanged(object sender, EventArgs e)
        {
            tbxFileName.Text = replaceFileName(tbxFileName.Text);
        }

        private string replaceFileName(string fileName)
        {
            try
            {
                Regex regex = new Regex(string.Format("[{0}]", Regex.Escape(new string(Path.GetInvalidFileNameChars()))));
                fileName = regex.Replace(fileName, " ");

                for (int i = 0; i < fileName.Length; i++)
                {
                    if (fileName[fileName.Length - i - 1] == '.')
                    {
                        fileName = fileName.Substring(0, fileName.Length - i - 1);
                        i = -1;
                    }
                    else
                        break;
                }

                if (fileName[fileName.Length - 1] == ' ')
                    fileName = fileName.Remove(fileName.Length - 1, 1);
            }
            catch (Exception exc)
            {
                
            }
            finally
            {
            }

            return fileName;
        }
    }
}
