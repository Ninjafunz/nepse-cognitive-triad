-- =============================================================================
-- Migration 002: Daily Decision Matrix & Epistemic Reflection Engine
-- =============================================================================

CREATE TABLE IF NOT EXISTS daily_evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    eval_date DATE NOT NULL DEFAULT CURRENT_DATE,
    symbol VARCHAR(10) NOT NULL,
    sector VARCHAR(50),
    
    -- The Triad Scores
    alpha_score NUMERIC(5,2) NOT NULL,
    beta_score NUMERIC(5,2) NOT NULL,
    gamma_score NUMERIC(5,2) NOT NULL,
    gamma_veto BOOLEAN DEFAULT FALSE NOT NULL,
    
    -- Final Action: BUY, SELL, HOLD, NO_ACTION
    final_action VARCHAR(20) NOT NULL,
    
    -- Qualitative Strategic Reason
    primary_reason TEXT NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT uq_daily_eval_date_symbol UNIQUE (eval_date, symbol)
);

CREATE INDEX IF NOT EXISTS idx_daily_eval_date ON daily_evaluations(eval_date);
CREATE INDEX IF NOT EXISTS idx_daily_eval_action ON daily_evaluations(final_action);
CREATE INDEX IF NOT EXISTS idx_daily_eval_symbol ON daily_evaluations(symbol);

-- The Epistemic Reflection Engine
CREATE TABLE IF NOT EXISTS prediction_reflections (
    reflection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID REFERENCES daily_evaluations(evaluation_id) ON DELETE CASCADE,
    
    symbol VARCHAR(10) NOT NULL,
    prediction_date DATE NOT NULL,
    target_date DATE NOT NULL, -- T+5 trading days later
    
    -- What the AI thought would happen
    predicted_thesis TEXT NOT NULL,
    expected_direction VARCHAR(10) NOT NULL, -- UP / DOWN
    
    -- Actual Market Outcome
    actual_return_pct NUMERIC(5,2),
    was_correct BOOLEAN,
    
    -- The AI's Post-Mortem Self-Correction Report
    reflection_journal TEXT,
    failed_route VARCHAR(20), -- ALPHA, BETA, GAMMA
    epistemic_concept VARCHAR(100), -- e.g., Shiller Narrative Illusion, Taleb Fragility
    corrective_action TEXT,
    
    reflected_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_target_date ON prediction_reflections(target_date);
CREATE INDEX IF NOT EXISTS idx_prediction_was_correct ON prediction_reflections(was_correct);
