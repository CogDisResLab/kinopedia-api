import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_stk33_rejection():
    """Test that STK33 (pseudokinase) rejects substrate creation"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Find STK33's ID
        list_response = await client.get("/kinases/")
        kinases = list_response.json()
        stk33 = next((k for k in kinases if k["hgnc_symbol"] == "STK33"), None)
        
        if stk33:
            # Try to add substrate
            response = await client.post("/substrates/", json={
                "kinase_id": stk33["kinase_id"],
                "substrate_gene": "TEST_GENE",
                "evidence_source": "test",
                "curator_confidence": "low"
            })
            
            assert response.status_code == 403
            assert "pseudokinase" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_create_substrate_valid():
    """Test creating a valid substrate for AKT1"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Find AKT1
        list_response = await client.get("/kinases/")
        kinases = list_response.json()
        akt1 = next((k for k in kinases if k["hgnc_symbol"] == "AKT1"), None)
        
        if akt1:
            # Create substrate
            response = await client.post("/substrates/", json={
                "kinase_id": akt1["kinase_id"],
                "substrate_gene": "TEST_GENE_UNIQUE",
                "phospho_site": "S999",
                "evidence_source": "test",
                "curator_confidence": "low"
            })
            
            # Should succeed (201) or conflict if already exists (409)
            assert response.status_code in [201, 409]