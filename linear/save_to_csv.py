import csv


class CSVWriter:
    @staticmethod
    def save_to_csv(data, filename="scraped_emails.csv"):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Write the header row
                writer.writerow(["Contact Page URL", "Emails"])
                
                # Write each contact URL and its associated emails
                for contact_url, emails in data.items():
                    writer.writerow([contact_url, "; ".join(emails)])

            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
