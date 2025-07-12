import asyncio
import aiohttp
import random
import time
from datetime import date, timedelta

class AsyncEmployeePoster:
    def __init__(self, url: str):
        self.url = url

    async def post_employee(self, session, employee_data, idx):
        try:
            async with session.post(self.url, json=employee_data) as resp:
                resp.raise_for_status()
                data = await resp.json()
                print(f"Employee {idx} posted: {data}")
                return data
        except aiohttp.ClientError as e:
            print(f"Request failed for employee {idx}:{resp} - {e}")
        except Exception as e:
            print(f"Unexpected error for employee {idx}: {e}")

    async def post_multiple_employees(self, employees):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.post_employee(session, emp, idx)
                for idx, emp in enumerate(employees, 1)
            ]
            return await asyncio.gather(*tasks)

    @staticmethod
    def generate_employees(n):
        # Dummy employee data generator
        return [
            {
                "name": f"Employee{idx}",
                "email": f"employee{idx}@example.com",
                "position": f"Position {idx % 5 + 1}",
                "startDate": (date.today() - timedelta(days=idx*10)).isoformat(),
                "endDate": (date.today() + timedelta(days=idx*365)).isoformat() 
            }
            for idx in range(1, n + 1)
        ]


if __name__ == "__main__":
    poster = AsyncEmployeePoster("http://127.0.0.1:8000/employees/")
    employees = poster.generate_employees(5)
    asyncio.run(poster.post_multiple_employees(employees))