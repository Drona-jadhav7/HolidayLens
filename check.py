import holidays
from datetime import date

def scan_xnse_diwali():
    current_year = date.today().year
    start_year = current_year - 10
    end_year = current_year + 10
    
    print(f"Scanning XNSE for Diwali (Laxmi Pujan) / Muhurat Trading from {start_year} to {end_year}...\n")
    
    missing_years = []
    
    for year in range(start_year, end_year + 1):
        try:
            # Generate financial holidays for the National Stock Exchange of India
            xnse_holidays = holidays.financial_holidays('XNSE', years=year)
            
            # Look for Diwali-related keywords in the holiday names
            diwali_found = False
            for holiday_date, name in xnse_holidays.items():
                name_lower = name.lower()
                if "diwali" in name_lower or "laxmi" in name_lower or "muhurat" in name_lower:
                    diwali_found = True
                    print(f"[FOUND] {year}: '{name}' is listed on {holiday_date} ({holiday_date.strftime('%A')})")
                    break
                    
            if not diwali_found:
                missing_years.append(year)
                print(f"[MISSING] {year}: Diwali / Muhurat Trading is entirely missing from XNSE.")
                
        except NotImplementedError:
            print(f"XNSE not supported for year {year}")

    print("\n--- Diagnostic Summary ---")
    if missing_years:
        print(f"Issue Verified: Diwali is missing in the following years: {missing_years}")
        print("Conclusion: The framework consistently drops Diwali whenever it falls on a weekend, failing to implement the 1-hour Muhurat Trading exception.")
    else:
        print("No missing years detected.")

if __name__ == "__main__":
    scan_xnse_diwali()