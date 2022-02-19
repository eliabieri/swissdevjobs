from pydantic import BaseModel, parse_raw_as
from typing import Optional
from rich.table import Table
from rich.console import Console
from datetime import datetime
import requests

class JobPost(BaseModel):
    name: str
    company: str
    cityCategory: str
    activeFrom: datetime
    offerStockOrBonus: Optional[bool]
    technologies: list[str]
    redirectJobUrl: Optional[str]
    jobType: Optional[str]
    annualSalaryFrom: Optional[int]
    annualSalaryTo: Optional[int]

def main():
    r = requests.get("https://swissdevjobs.ch/api/jobsLight")
    jobs = parse_raw_as(list[JobPost], r.text)

    parttimeJobs = list(filter(lambda p: p.jobType == "Part-Time" ,jobs))

    bestPayingJob = max(jobs, key=lambda k: k.annualSalaryTo or 0)
    funFact = f"Fun fact: The highest salary on swissdevjobs.ch currently is {bestPayingJob.annualSalaryTo} CHF ({bestPayingJob.name})"

    table = Table(title=f"{len(parttimeJobs)} Part-Time Jobs.\n{funFact}")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Company", justify="left", style="yellow", no_wrap=True)
    table.add_column("City", justify="left", style="green", no_wrap=True)
    table.add_column("Annual salary", style="magenta")
    table.add_column("Technologies", style="red")
    table.add_column("Active from")
    table.add_column("URL")


    for job in parttimeJobs:
        name = f"{job.name} {'💎' if job.offerStockOrBonus else ''}"
        salary = f"{job.annualSalaryFrom} - {job.annualSalaryTo} CHF"
        activeFrom = job.activeFrom.strftime("%A %d. %B %H:%M")
        technologies = ", ".join(job.technologies)
        table.add_row(name, job.company, job.cityCategory, salary, technologies, activeFrom, f"[link={job.redirectJobUrl}]Click 🔗[/link]")

    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()