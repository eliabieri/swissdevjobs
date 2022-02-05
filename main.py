from pydantic import BaseModel, parse_raw_as
from typing import Optional
from rich.table import Table
from rich.console import Console
from datetime import datetime
import requests

class JobPost(BaseModel):
    name: str
    company: str
    activeFrom: datetime
    redirectJobUrl: Optional[str]
    jobType: Optional[str]
    annualSalaryFrom: Optional[int]
    annualSalaryTo: Optional[int]

def main():
    r = requests.get("https://swissdevjobs.ch/api/jobsLight")
    jobs = parse_raw_as(list[JobPost], r.text)

    jobs = list(filter(lambda p: p.jobType == "Part-Time" ,jobs))

    table = Table(title=f"{len(jobs)} Part-Time Jobs")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Company", justify="left", style="yellow", no_wrap=True)
    table.add_column("Annual salary from", style="magenta")
    table.add_column("Annual salary to", style="green")
    table.add_column("Active from")
    table.add_column("URL")

    for job in jobs:
        salaryFrom = str(job.annualSalaryFrom) if job.annualSalaryFrom else "-"
        salaryTo = str(job.annualSalaryTo) if job.annualSalaryTo else "-"
        table.add_row(job.name, job.company, salaryFrom, salaryTo, job.activeFrom.strftime("%A %d. %B %H:%M"), job.redirectJobUrl)

    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()