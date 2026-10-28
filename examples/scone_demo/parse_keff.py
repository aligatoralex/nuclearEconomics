"""Extract the final k-eff from a SCONE log and print it as CSV."""
import re
import sys

text = open(sys.argv[1]).read()
matches = re.findall(r"k-eff \(implicit\):\s+([\d.]+) \+/-\s+([\d.]+)", text)
if not matches:
    sys.exit("no k-eff found in log")
k, sigma = matches[-1]
print("k_eff,sigma")
print(f"{k},{sigma}")
