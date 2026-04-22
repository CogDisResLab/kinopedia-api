import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_list_kinases():
    """Test that we can list all kinases"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/kinases/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8  # We have 8 kinases

@pytest.mark.asyncio
async def test_get_kinase_detail():
    """Test getting details for a specific kinase"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First get list to find a kinase ID
        list_response = await client.get("/kinases/")
        kinases = list_response.json()
        kinase_id = kinases[0]["kinase_id"]
        
        # Get detail
        response = await client.get(f"/kinases/{kinase_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "hgnc_symbol" in data
    assert "substrate_count" in data

@pytest.mark.asyncio
async def test_kinase_not_found():
    """Test 404 for non-existent kinase"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/kinases/fake-id-12345")
    
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_substrates():
    """Test getting substrates for a kinase"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get AKT1 (should have substrates)
        list_response = await client.get("/kinases/")
        kinases = list_response.json()
        akt1 = next((k for k in kinases if k["hgnc_symbol"] == "AKT1"), None)
        
        if akt1:
            response = await client.get(f"/kinases/{akt1['kinase_id']}/substrates")
            assert response.status_code == 200
            substrates = response.json()
            assert len(substrates) > 0