#!/usr/bin/env python3
"""
Debug script to test the CASE hierarchy parser
"""
import asyncio
import sys
sys.path.insert(0, '/Users/colossus/development/content/backend')

from services.standards_importer import CASEParser

async def main():
    parser = CASEParser()

    # Test with Georgia Math
    url = "https://case.georgiastandards.org/ims/case/v1p0/CFPackages/e9dd7229-3558-4df2-85c6-57b8938f6180"

    print("Fetching Georgia Math CASE data...")
    result = await parser.parse(url)

    print("\nParse Results:")
    print(f"Name: {result['name']}")
    print(f"Total Standards: {result['total_standards_count']}")

    structure = result['structure']
    domains = structure.get('domains', [])

    print(f"\nHierarchical Structure:")
    print(f"Total Domains: {len(domains)}")

    if domains:
        print("\nDomains:")
        for i, domain in enumerate(domains[:3]):
            print(f"\n{i+1}. {domain.get('name', 'Unnamed')[:60]}")
            print(f"   ID: {domain.get('id', 'No ID')}")
            print(f"   Strands: {len(domain.get('strands', []))}")

            for j, strand in enumerate(domain.get('strands', [])[:2]):
                print(f"     {j+1}. {strand.get('name', 'Unnamed')[:50]}")
                print(f"        Standards: {len(strand.get('standards', []))}")
    else:
        print("⚠️  No domains created!")

        # Check if we got standards in the flat list
        if result['standards_list']:
            print(f"\nBut we have {len(result['standards_list'])} standards in flat list:")
            for i, std in enumerate(result['standards_list'][:3]):
                print(f"  {i+1}. {std['code']}: {std['text'][:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
