using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LogParserGUI
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void btnBrowseInput_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                txtInput.Text = openFileDialog.FileName;
            }

        }

        private void btnBrowseOutput_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "CSV File|*.csv";
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                txtOutput.Text = saveFileDialog.FileName;
            }
        }

        private void btnRun_Click(object sender, EventArgs e)
        {
            string pythonPath = "python"; 
            
            string scriptPath = @"C:\Users\Black\IdeaProjects\Personal-Projects\In-progress\log_aggregator_analyzer\log_parser.py";

            string inputFile = txtInput.Text;
            string outputFile = txtOutput.Text;
            string limit = columnLimit.Text;

            if (string.IsNullOrEmpty(inputFile))
            {
                MessageBox.Show("Please select the input file first!");
                return;
            }

           
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = pythonPath;
            
            start.Arguments = string.Format("\"{0}\" \"{1}\" \"{2}\" {3}",
                                            scriptPath, inputFile, outputFile, limit);

            start.UseShellExecute = false; 
            start.RedirectStandardOutput = true;
            start.CreateNoWindow = true; 

       
            try
            {
                using (Process process = Process.Start(start))
                {
      
                    using (System.IO.StreamReader reader = process.StandardOutput)
                    {
                        string result = reader.ReadToEnd();
                        process.WaitForExit(); 

       
                        MessageBox.Show("Python Output:\n" + result, "Success");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error running Python:\n" + ex.Message);
            }
        }
    }
}
