import pytest
import asyncio
import time
import httpx
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_bulk_indexing_and_search():
    """Simple test to index documents and search for them in bulk"""
    
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        schema_payload = {
            "name": "products",
            "fields": [
                {"name": "title", "type": "text", "sortable": True, "weight": 2.0},
                {"name": "price", "type": "numeric", "sortable": True}
            ]
        }
        
        res_schema = await client.post("/schemas/", json=schema_payload)
        assert res_schema.status_code == 200
        print("-> Schema created successfully")
        
        print("-> Indexing 1000 documents...")
        start_time = time.perf_counter()
        
        tasks = []
        for i in range(1000):
            product_payload = {
                "schema_name": "products",
                "document_id": str(i),
                "fields": {
                    "title": f"Laptop {i}",
                    "price": i * 10
                }
            }
            tasks.append(client.post("/documents/", json=product_payload))
        
        # Execute all index operations in parallel
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        index_time = time.perf_counter() - start_time
        
        # Check results of indexing
        successful = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code == 200)
        failed = len(responses) - successful
        
        # Print details about failed requests
        if failed > 0:
            print(f"-> Failed requests details:")
            failed_count = 0
            for i, r in enumerate(responses):
                if isinstance(r, Exception):
                    print(f"  Request {i}: Exception - {str(r)}")
                    failed_count += 1
                elif r.status_code != 200:
                    print(f"  Request {i}: Status {r.status_code} - {r.text}")
                    failed_count += 1
                if failed_count >= 10:  # Limit output to first 10 failures
                    print(f"  ... and {failed - failed_count} more failures")
                    break
        
        print(f"-> Indexing: {successful} successes, {failed} fails")
        print(f"-> Time: {index_time:.2f}s")
        print(f"-> Rate: {successful/index_time:.2f} docs/s")
        
        assert failed == 0, f"Failed {failed} indexings"
        assert successful == 1000
        
        # Wait a little to ensure indexing
        await asyncio.sleep(1)
        
        # Test bulk search
        print("-> Testing bulk search...")
        search_start = time.perf_counter()
        
        # Make 50 concurrent searches
        search_tasks = []
        for _ in range(50):
            search_tasks.append(client.get("/documents/search/", params={
                "schema_name": "products",
                "term": "Laptop",
                "limit": 10,
                "offset": 0
            }))
        
        search_responses = await asyncio.gather(*search_tasks, return_exceptions=True)
        search_time = time.perf_counter() - search_start
        
        # Check results of search
        search_successful = sum(1 for r in search_responses if not isinstance(r, Exception) and r.status_code == 200)
        search_failed = len(search_responses) - search_successful
        
        print(f"-> Search: {search_successful} sucess, {search_failed} failed")
        print(f"-> Time: {search_time:.2f}s")
        print(f"-> Rate: {search_successful/search_time:.2f} searches/s")
        
        assert search_failed == 0, f"Failed {search_failed} searches"
        assert search_successful == 50
        
        # Check if the search returns results
        if search_responses and not isinstance(search_responses[0], Exception):
            first_search = search_responses[0]
            if first_search.status_code == 200:
                data = first_search.json()
                total_results = data["data"]["total"]
                print(f"-> Total results: {total_results}")
                assert total_results > 0, "No results found in search"
        
        print("-> Test completed successfully")
