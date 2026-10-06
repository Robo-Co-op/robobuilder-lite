from pathlib import Path


def test_ship_checks_current_head_before_merge():
    text = (Path(__file__).resolve().parents[2] / 'skills/ship/SKILL.md').read_text()
    land = text.split('### Stage 3 — Land')[1].split('### Stage 4')[0]
    assert land.index('exact SHA') < land.index('2. **Merge')
    assert 'independent review' in land and 'all required approvals' in land
    assert 'changed head invalidates readiness' in land
    assert 'only within the user\'s authorized scope' in land
    assert 'additional check, never a substitute' in land
