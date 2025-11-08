#!/usr/bin/env python3
"""
Detailed debug of CASE hierarchy parsing
"""
import aiohttp
import asyncio

async def main():
    url = "https://case.georgiastandards.org/ims/case/v1p0/CFPackages/e9dd7229-3558-4df2-85c6-57b8938f6180"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    cf_items = data.get("CFItems", [])
    cf_associations = data.get("CFAssociations", [])

    print(f"Total CFItems: {len(cf_items)}")
    print(f"Total CFAssociations: {len(cf_associations)}")

    # Build items lookup
    items_by_id = {item["identifier"]: item for item in cf_items}

    # Build parent-child relationships
    children_by_parent = {}
    for assoc in cf_associations:
        if assoc.get("associationType") == "isChildOf":
            parent_id = assoc.get("destinationNodeURI", {}).get("identifier")
            child_id = assoc.get("originNodeURI", {}).get("identifier")

            if parent_id not in children_by_parent:
                children_by_parent[parent_id] = []
            children_by_parent[parent_id].append(child_id)

    print(f"\nParent nodes with children: {len(children_by_parent)}")

    # Find root items
    all_child_ids = set()
    for children in children_by_parent.values():
        all_child_ids.update(children)

    root_items = []
    for item_id in items_by_id.keys():
        if item_id not in all_child_ids:
            root_items.append(item_id)

    print(f"Root items found: {len(root_items)}")

    # Examine root items
    print("\nRoot Items:")
    for i, root_id in enumerate(root_items[:5]):
        root_item = items_by_id.get(root_id)
        code = root_item.get("humanCodingScheme", "NO CODE")
        text = root_item.get("fullStatement", "NO TEXT")[:50]
        title = root_item.get("title", "NO TITLE")[:50]
        has_children = len(children_by_parent.get(root_id, []))

        print(f"\n  {i+1}. ID: {root_id[:20]}...")
        print(f"     Code: {code}")
        print(f"     Text: {text}...")
        print(f"     Title: {title}...")
        print(f"     Children: {has_children}")

        # Check if this root has standards as children
        children = children_by_parent.get(root_id, [])
        if children:
            print(f"     First 3 children:")
            for j, child_id in enumerate(children[:3]):
                child = items_by_id.get(child_id)
                child_code = child.get("humanCodingScheme", "NO CODE")
                child_text = child.get("fullStatement", "NO TEXT")[:30]
                print(f"       - {child_code}: {child_text}...")

if __name__ == "__main__":
    asyncio.run(main())
