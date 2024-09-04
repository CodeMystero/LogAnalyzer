
namespace CustomWireshark
{
    partial class FormSettings
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.lbLogSavePath = new System.Windows.Forms.Label();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.cbLogLevel = new System.Windows.Forms.ComboBox();
            this.btnLogPath = new System.Windows.Forms.Button();
            this.chkEnableLog = new System.Windows.Forms.CheckBox();
            this.btnOk = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.btnDumpPath = new System.Windows.Forms.Button();
            this.lbDumpSavePath = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.lbFileName = new System.Windows.Forms.Label();
            this.tbxFileName = new System.Windows.Forms.TextBox();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(6, 54);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(61, 12);
            this.label1.TabIndex = 0;
            this.label1.Text = "Save path";
            // 
            // lbLogSavePath
            // 
            this.lbLogSavePath.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbLogSavePath.Location = new System.Drawing.Point(8, 72);
            this.lbLogSavePath.Name = "lbLogSavePath";
            this.lbLogSavePath.Size = new System.Drawing.Size(250, 44);
            this.lbLogSavePath.TabIndex = 4;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.cbLogLevel);
            this.groupBox1.Controls.Add(this.btnLogPath);
            this.groupBox1.Controls.Add(this.chkEnableLog);
            this.groupBox1.Controls.Add(this.lbLogSavePath);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(266, 128);
            this.groupBox1.TabIndex = 2;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Log";
            // 
            // cbLogLevel
            // 
            this.cbLogLevel.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbLogLevel.FormattingEnabled = true;
            this.cbLogLevel.Items.AddRange(new object[] {
            "Error",
            "Warn",
            "Debug",
            "Info"});
            this.cbLogLevel.Location = new System.Drawing.Point(137, 18);
            this.cbLogLevel.Name = "cbLogLevel";
            this.cbLogLevel.Size = new System.Drawing.Size(121, 20);
            this.cbLogLevel.TabIndex = 2;
            // 
            // btnLogPath
            // 
            this.btnLogPath.Location = new System.Drawing.Point(233, 44);
            this.btnLogPath.Name = "btnLogPath";
            this.btnLogPath.Size = new System.Drawing.Size(25, 25);
            this.btnLogPath.TabIndex = 3;
            this.btnLogPath.Text = "...";
            this.btnLogPath.UseVisualStyleBackColor = true;
            this.btnLogPath.Click += new System.EventHandler(this.btnLogPath_Click);
            // 
            // chkEnableLog
            // 
            this.chkEnableLog.AutoSize = true;
            this.chkEnableLog.Location = new System.Drawing.Point(8, 20);
            this.chkEnableLog.Name = "chkEnableLog";
            this.chkEnableLog.Size = new System.Drawing.Size(95, 16);
            this.chkEnableLog.TabIndex = 1;
            this.chkEnableLog.Text = "Enable Save";
            this.chkEnableLog.UseVisualStyleBackColor = true;
            // 
            // btnOk
            // 
            this.btnOk.Location = new System.Drawing.Point(30, 284);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(113, 48);
            this.btnOk.TabIndex = 5;
            this.btnOk.Text = "OK";
            this.btnOk.UseVisualStyleBackColor = true;
            this.btnOk.Click += new System.EventHandler(this.btnOk_Click);
            // 
            // btnCancel
            // 
            this.btnCancel.Location = new System.Drawing.Point(149, 284);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(113, 48);
            this.btnCancel.TabIndex = 6;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.tbxFileName);
            this.groupBox2.Controls.Add(this.lbFileName);
            this.groupBox2.Controls.Add(this.btnDumpPath);
            this.groupBox2.Controls.Add(this.lbDumpSavePath);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Location = new System.Drawing.Point(12, 146);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(266, 132);
            this.groupBox2.TabIndex = 2;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "pcapng Dump";
            // 
            // btnDumpPath
            // 
            this.btnDumpPath.Location = new System.Drawing.Point(233, 50);
            this.btnDumpPath.Name = "btnDumpPath";
            this.btnDumpPath.Size = new System.Drawing.Size(25, 25);
            this.btnDumpPath.TabIndex = 3;
            this.btnDumpPath.Text = "...";
            this.btnDumpPath.UseVisualStyleBackColor = true;
            this.btnDumpPath.Click += new System.EventHandler(this.btnDumpPath_Click);
            // 
            // lbDumpSavePath
            // 
            this.lbDumpSavePath.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbDumpSavePath.Location = new System.Drawing.Point(8, 78);
            this.lbDumpSavePath.Name = "lbDumpSavePath";
            this.lbDumpSavePath.Size = new System.Drawing.Size(250, 44);
            this.lbDumpSavePath.TabIndex = 4;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(6, 60);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(61, 12);
            this.label3.TabIndex = 0;
            this.label3.Text = "Save path";
            // 
            // lbFileName
            // 
            this.lbFileName.AutoSize = true;
            this.lbFileName.Location = new System.Drawing.Point(8, 26);
            this.lbFileName.Name = "lbFileName";
            this.lbFileName.Size = new System.Drawing.Size(123, 12);
            this.lbFileName.TabIndex = 5;
            this.lbFileName.Text = "File name(*.pcapng)";
            // 
            // tbxFileName
            // 
            this.tbxFileName.Location = new System.Drawing.Point(137, 23);
            this.tbxFileName.Name = "tbxFileName";
            this.tbxFileName.Size = new System.Drawing.Size(121, 21);
            this.tbxFileName.TabIndex = 6;
            this.tbxFileName.TextChanged += new System.EventHandler(this.tbxFileName_TextChanged);
            // 
            // FormSettings
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(290, 340);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "FormSettings";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Settings";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lbLogSavePath;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button btnLogPath;
        private System.Windows.Forms.CheckBox chkEnableLog;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.ComboBox cbLogLevel;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button btnDumpPath;
        private System.Windows.Forms.Label lbDumpSavePath;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox tbxFileName;
        private System.Windows.Forms.Label lbFileName;
    }
}