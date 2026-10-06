from pathlib import Path


def test_ship_checks_current_head_before_merge():
    text = (Path(__file__).resolve().parents[2] / 'skills/ship/SKILL.md').read_text()
    land = text.split('### Stage 3 — Land')[1].split('### Stage 4')[0]
    assert land.index('exact SHA') < land.index('2. **Merge')
    assert 'independent review' in land and 'all required approvals' in land
    assert 'changed head invalidates readiness' in land
    assert 'only within the user\'s authorized scope' in land
    assert 'additional check, never a substitute' in land


def test_pending_review_request_does_not_waive_merge_review():
    root = Path(__file__).resolve().parents[2]
    improve = (root / 'skills/improve/SKILL.md').read_text()
    ship = (root / 'skills/ship/SKILL.md').read_text()
    assert 'needs_human_review' in improve and '**PENDING**' in improve
    assert 'does not complete improve or authorize merge/deploy' in improve
    assert 'keep the verdict `PENDING` / `needs_human_review`' in ship
    assert 'stop before Land' in ship
    assert 'If publication itself is blocked' in ship
