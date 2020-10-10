using System;
using System.Diagnostics;

namespace SPTagPOC
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("-- Program started ----");

            var psi = new ProcessStartInfo();

            ////For local
            //psi.FileName = "py";

            //For release
            psi.FileName = "python3";

            //"BuildIndexAndSearchOffline.py" or "IndexSearchOnline.py"
            var pythonFileName = "IndexSearchOnline.py";
            var aggregatorIp = "52.255.166.26";
            var aggregatorPort = "8100";

            //var pythonArgs = "";
            var pythonArgs = $"\"{aggregatorIp}\" \"{aggregatorPort}\"";

            psi.Arguments = $"{pythonFileName} {pythonArgs}";

            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.RedirectStandardInput = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            var error = string.Empty;
            var result = string.Empty;

            using (var process = Process.Start(psi))
            {
                error = process.StandardError.ReadToEnd();
                result = process.StandardOutput.ReadToEnd();
            }

            Console.WriteLine($"Error: {error}");
            Console.WriteLine($"Result: {result}");

            Console.WriteLine("-- Program completed ----");


            Console.Read();
        }
    }
}
