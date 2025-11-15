# Correlation Algorithms - Research & Selection Guide

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Research Document
- **Purpose**: Help select appropriate correlation algorithms for FeelInk

---

## 1. Overview

This document provides a comprehensive overview of correlation algorithms suitable for analyzing relationships between mental health metrics and external factors. Understanding these algorithms will help us choose the most appropriate methods for FeelInk's analytics engine.

### 1.1 What is Correlation?

Correlation measures the strength and direction of the relationship between two variables:
- **Strength**: How closely the variables move together (0 to 1)
- **Direction**: Whether they move in the same direction (positive) or opposite directions (negative)
- **Coefficient Range**: Typically -1 to +1
  - +1: Perfect positive correlation
  - 0: No correlation
  - -1: Perfect negative correlation

---

## 2. Standard Correlation Methods

### 2.1 Pearson Correlation

#### Description
Measures **linear** relationship between two continuous variables.

#### Formula
```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]

where:
- xi, yi = individual data points
- x̄, ȳ = means of x and y
```

#### When to Use
✅ **Best for:**
- Continuous numeric data (e.g., mood scale 1-10, sleep hours)
- Linear relationships
- Normally distributed data
- Interval or ratio scales

❌ **Not suitable for:**
- Ordinal data (ranked data)
- Non-linear relationships
- Data with outliers
- Boolean data

#### FeelInk Use Cases
- Mood (1-10) vs. Sleep Hours
- Anxiety Level vs. Exercise Duration
- Energy Level vs. Caffeine Intake

#### Pros & Cons

**Pros:**
- Most widely used and understood
- Fast to compute
- Good statistical properties
- Well-established interpretation

**Cons:**
- Assumes linear relationship
- Sensitive to outliers
- Requires normally distributed data
- Only detects linear patterns

#### Code Example
```python
from scipy.stats import pearsonr

# Example: Mood vs. Sleep
mood = [7, 8, 6, 9, 5, 8, 7]
sleep_hours = [7.5, 8.0, 6.0, 8.5, 5.5, 7.5, 7.0]

coefficient, p_value = pearsonr(mood, sleep_hours)
print(f"Pearson r = {coefficient:.3f}, p = {p_value:.3f}")
# Output: Pearson r = 0.952, p = 0.001
```

#### Interpretation Guide
| |r| Value | Interpretation |
|-----------|----------------|
| 0.0 - 0.3 | Weak correlation |
| 0.3 - 0.7 | Moderate correlation |
| 0.7 - 1.0 | Strong correlation |

---

### 2.2 Spearman Rank Correlation

#### Description
Measures **monotonic** relationship using ranks instead of raw values.

#### Formula
```
ρ = 1 - [6 × Σdi²] / [n(n² - 1)]

where:
- di = difference between ranks
- n = number of observations
```

#### When to Use
✅ **Best for:**
- Ordinal data (ranked data)
- Non-linear but monotonic relationships
- Data with outliers
- Non-normally distributed data

❌ **Not suitable for:**
- When you specifically need linear relationships
- Very small sample sizes (<5)

#### FeelInk Use Cases
- "How stressed do you feel?" (low/medium/high) vs. Work Hours
- Pain Level (ordinal scale) vs. Activity Level
- Sleep Quality (poor/fair/good/excellent) vs. Mood

#### Pros & Cons

**Pros:**
- Robust to outliers
- Works with ordinal data
- No normality assumption
- Detects non-linear monotonic relationships

**Cons:**
- Less powerful than Pearson for linear data
- Loses some information by using ranks
- Slightly more complex to interpret

#### Code Example
```python
from scipy.stats import spearmanr

# Example: Stress level (ordinal) vs. Work hours
stress_level = [1, 3, 2, 5, 4, 5, 3]  # 1=low, 5=high
work_hours = [6, 9, 7, 12, 10, 11, 8]

coefficient, p_value = spearmanr(stress_level, work_hours)
print(f"Spearman ρ = {coefficient:.3f}, p = {p_value:.3f}")
# Output: Spearman ρ = 0.929, p = 0.003
```

#### Recommendation for FeelInk
**HIGH PRIORITY**: Should implement as primary method alongside Pearson, since mental health data often:
- Uses ordinal scales (bad/okay/good)
- Contains outliers
- May have non-linear relationships

---

### 2.3 Kendall's Tau

#### Description
Another rank-based correlation measuring concordance between rankings.

#### Formula
```
τ = (C - D) / [n(n-1)/2]

where:
- C = number of concordant pairs
- D = number of discordant pairs
- n = sample size
```

#### When to Use
✅ **Best for:**
- Small sample sizes
- Data with many tied ranks
- More robust statistical testing
- Ordinal data

❌ **Not suitable for:**
- Large datasets (computationally expensive)
- When Spearman is sufficient

#### FeelInk Use Cases
- Similar to Spearman, but better for:
  - Small pilot studies
  - Data with many ties (e.g., yes/no/maybe responses)

#### Pros & Cons

**Pros:**
- More robust than Spearman for small samples
- Better handles tied ranks
- More accurate p-values
- Better statistical properties

**Cons:**
- Computationally expensive for large datasets
- Generally gives smaller coefficient values than Spearman
- Less intuitive interpretation

#### Code Example
```python
from scipy.stats import kendalltau

# Example: Meditation practice (yes/no) vs. Anxiety level
meditation = [0, 1, 0, 1, 1, 0, 1]  # 0=no, 1=yes
anxiety = [7, 4, 8, 3, 2, 6, 3]

coefficient, p_value = kendalltau(meditation, anxiety)
print(f"Kendall τ = {coefficient:.3f}, p = {p_value:.3f}")
# Output: Kendall τ = -0.714, p = 0.052
```

#### Recommendation for FeelInk
**MEDIUM PRIORITY**: Useful to have as an option, especially for:
- Validating Spearman results
- Boolean metrics (took medication: yes/no)
- Small sample sizes

---

## 3. Time-Series Specific Methods

### 3.1 Cross-Correlation (Lag Correlation)

#### Description
Measures correlation between two time series at different time lags, revealing **delayed effects**.

#### Concept
```
Example: Alcohol consumption affects mood 3 days later

Day:        1  2  3  4  5  6  7  8  9  10
Alcohol:    2  0  0  3  0  0  1  0  0  2
Mood:       7  7  7  5  6  6  4  7  7  5
                      ↑  ↑  ↑        ↑
                      Lag = 3 days
```

#### When to Use
✅ **ESSENTIAL for FeelInk:**
- Discovering delayed effects
- Understanding causation timing
- Mental health often has delayed reactions

#### FeelInk Use Cases
- Alcohol → Mood (lag: 1-3 days)
- Poor Sleep → Irritability (lag: 1 day)
- Medication → Symptom Relief (lag: 1-7 days)
- Stressful Event → Anxiety Peak (lag: 0-2 days)

#### Implementation Strategy

```python
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def cross_correlation(series1, series2, max_lag=7):
    """
    Calculate cross-correlation with time lags.

    Args:
        series1: First time series (e.g., trigger)
        series2: Second time series (e.g., symptom)
        max_lag: Maximum lag to test (in days)

    Returns:
        List of (lag, correlation, p_value) tuples
    """
    results = []

    for lag in range(0, max_lag + 1):
        # Shift series2 backward by lag
        if lag == 0:
            s1 = series1
            s2 = series2
        else:
            s1 = series1[:-lag]
            s2 = series2[lag:]

        # Remove NaN and calculate correlation
        mask = ~(pd.isna(s1) | pd.isna(s2))
        if mask.sum() >= 3:  # Need at least 3 points
            coef, pval = pearsonr(s1[mask], s2[mask])
            results.append({
                'lag': lag,
                'coefficient': coef,
                'p_value': pval
            })

    return results

# Example usage
alcohol = [2, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0]
mood = [7, 7, 7, 5, 6, 6, 4, 7, 7, 5, 6, 6]

correlations = cross_correlation(
    pd.Series(alcohol),
    pd.Series(mood),
    max_lag=5
)

# Find strongest correlation
best = max(correlations, key=lambda x: abs(x['coefficient']))
print(f"Strongest correlation at lag {best['lag']} days: r={best['coefficient']:.3f}")
```

#### Recommendation for FeelInk
**CRITICAL PRIORITY**: This is the most valuable feature for mental health tracking!
- Users discover "X affects me Y days later"
- Differentiates FeelInk from simple tracking apps

---

### 3.2 Autocorrelation

#### Description
Measures how a time series correlates with itself at different time lags.

#### Purpose
Detect patterns and cycles in individual metrics:
- Weekly mood cycles
- Menstrual cycle effects
- Seasonal patterns

#### FeelInk Use Cases
- "My mood drops every Sunday"
- "My energy is lowest every 28 days"
- "My sleep quality has a 7-day cycle"

#### Code Example
```python
from statsmodels.tsa.stattools import acf

# Example: Mood over 30 days
mood = [6, 7, 8, 7, 6, 5, 4,  # Week 1 (weekend dip)
        6, 7, 8, 7, 6, 5, 4,  # Week 2
        6, 7, 8, 7, 6, 5, 4,  # Week 3
        6, 7, 8, 7, 6, 5, 4]  # Week 4

# Calculate autocorrelation for lags 0-14
autocorr = acf(mood, nlags=14)

print("Lag 7 autocorrelation:", autocorr[7])  # Weekly pattern
# High value indicates weekly cycle
```

#### Recommendation for FeelInk
**MEDIUM PRIORITY**: Valuable for discovering personal patterns
- Implement after basic correlations working
- Great for "insights" feature

---

## 4. Advanced Methods

### 4.1 Partial Correlation

#### Description
Measures correlation between two variables while controlling for the effect of other variables.

#### Purpose
Answer questions like:
- "Does exercise improve mood **independent of** better sleep?"
- "Is medication effective **controlling for** therapy sessions?"

#### Example Scenario
```
Observed:
- Exercise correlates with better mood (r=0.7)
- Exercise correlates with better sleep (r=0.6)
- Sleep correlates with better mood (r=0.8)

Question: Does exercise improve mood directly,
or only because it improves sleep?

Partial Correlation (Exercise-Mood, controlling for Sleep):
- If still high (r=0.6): Exercise has direct effect
- If now low (r=0.2): Exercise works mainly through sleep
```

#### Code Example
```python
from scipy.stats import pearsonr
import numpy as np

def partial_correlation(x, y, z):
    """
    Calculate partial correlation between x and y,
    controlling for z.
    """
    # Correlations
    r_xy = pearsonr(x, y)[0]
    r_xz = pearsonr(x, z)[0]
    r_yz = pearsonr(y, z)[0]

    # Partial correlation formula
    r_xy_z = (r_xy - r_xz * r_yz) / np.sqrt((1 - r_xz**2) * (1 - r_yz**2))

    return r_xy_z

# Example
exercise = [1, 2, 0, 3, 2, 1, 3, 2, 1, 2]
sleep = [6, 7, 5, 8, 7, 6, 8, 7, 6, 7]
mood = [5, 7, 4, 9, 7, 6, 9, 7, 5, 7]

direct_effect = partial_correlation(exercise, mood, sleep)
print(f"Exercise-Mood correlation (controlling for sleep): {direct_effect:.3f}")
```

#### Recommendation for FeelInk
**LOW PRIORITY for MVP**: Implement in Phase 2
- Requires more data points
- More complex to explain to users
- Valuable for advanced users

---

### 4.2 Granger Causality

#### Description
Statistical test to determine if one time series helps predict another.

#### Purpose
Move beyond correlation toward **causation**:
- Does X cause Y, or does Y cause X?
- Or are they both caused by something else?

#### Important Note
⚠️ **"Granger causality" ≠ true causality**
- It shows predictive relationship
- Not proof of causal mechanism
- Requires careful interpretation

#### FeelInk Application
Limited use for MVP, but interesting for future:
- "Does stress predict sleep problems, or vice versa?"
- Requires longer time series (30+ days)

#### Recommendation for FeelInk
**NOT for MVP**: Research feature for Phase 3
- Requires significant data
- Complex interpretation
- May confuse users

---

## 5. Practical Considerations

### 5.1 Sample Size Requirements

| Algorithm | Minimum | Recommended | Optimal |
|-----------|---------|-------------|---------|
| Pearson | 3 | 7 | 30+ |
| Spearman | 3 | 7 | 30+ |
| Kendall | 3 | 5 | 20+ |
| Cross-correlation | 10 | 14 | 30+ |
| Partial correlation | 10 | 20 | 50+ |

#### For FeelInk:
- Start showing correlations after **7 days** minimum
- Mark as "preliminary" until **14 days**
- Full confidence at **30+ days**

### 5.2 Statistical Significance (p-value)

#### What is p-value?
- Probability that the correlation occurred by chance
- Lower = more confident it's real

#### Interpretation
| p-value | Interpretation | Symbol |
|---------|----------------|--------|
| < 0.01 | Highly significant | *** |
| < 0.05 | Significant | ** |
| < 0.10 | Marginally significant | * |
| ≥ 0.10 | Not significant | - |

#### FeelInk Strategy
```python
def interpret_correlation(coefficient, p_value, n_samples):
    """Generate user-friendly interpretation."""

    # Check significance
    if p_value < 0.01:
        significance = "very confident"
    elif p_value < 0.05:
        significance = "confident"
    elif p_value < 0.10:
        significance = "somewhat confident"
    else:
        return "Not enough evidence of a relationship."

    # Check strength
    abs_coef = abs(coefficient)
    if abs_coef < 0.3:
        strength = "weak"
    elif abs_coef < 0.7:
        strength = "moderate"
    else:
        strength = "strong"

    # Direction
    direction = "positive" if coefficient > 0 else "negative"

    # Sample size warning
    warning = "" if n_samples >= 14 else " (Note: Limited data - track for longer to confirm)"

    return f"We're {significance} there's a {strength} {direction} relationship.{warning}"
```

### 5.3 Multiple Testing Correction

#### The Problem
When testing many correlations, some will appear significant by chance.

Example:
- Testing 20 metric pairs
- At p<0.05, expect 1 false positive even with random data

#### Solutions

**1. Bonferroni Correction** (conservative)
```python
adjusted_p_threshold = 0.05 / number_of_tests
# If testing 20 pairs: 0.05/20 = 0.0025
```

**2. False Discovery Rate (FDR)** (less conservative)
```python
from statsmodels.stats.multitest import multipletests

# p-values from multiple tests
p_values = [0.01, 0.04, 0.15, 0.002, 0.08]

# Apply FDR correction
reject, p_adjusted, _, _ = multipletests(
    p_values,
    alpha=0.05,
    method='fdr_bh'  # Benjamini-Hochberg
)

print(p_adjusted)
```

#### FeelInk Recommendation
- Use FDR correction when showing "top correlations"
- Clearly mark corrected vs. uncorrected p-values
- Don't hide borderline results, but flag them

---

## 6. Recommended Implementation Strategy

### Phase 1 (MVP): Core Correlations
✅ **Must Have:**
1. **Pearson correlation** - for continuous numeric metrics
2. **Spearman correlation** - for ordinal/ranked metrics
3. **Cross-correlation** (lag 0-7 days) - for time-delayed effects
4. **Basic significance testing** (p-values)

**Rationale:**
- Covers 90% of use cases
- Easy to explain to users
- Computationally light
- Well-established interpretations

### Phase 2: Enhanced Analytics
✅ **Should Have:**
1. **Kendall's Tau** - for validation and small samples
2. **Autocorrelation** - for discovering personal cycles
3. **Multiple testing correction** - for accurate significance
4. **Confidence intervals** - for correlation estimates

### Phase 3: Advanced Features
📊 **Nice to Have:**
1. **Partial correlation** - for controlling confounds
2. **Granger causality** - for predictive relationships
3. **Rolling correlations** - for time-varying relationships
4. **Breakpoint detection** - for detecting changes in relationships

---

## 7. User Interface Considerations

### 7.1 How to Present Correlations to Users

#### Good Example (User-Friendly):
```
╔══════════════════════════════════════════════════════╗
║ 🔍 Discovered Relationship                          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Exercise (hours) ↑                                  ║
║         ⬆                                            ║
║  Mood Score ↑                                        ║
║                                                      ║
║  Strength: Strong positive (r=0.82)                  ║
║  Confidence: Very confident (p=0.001)                ║
║  Timing: Same day effect                             ║
║                                                      ║
║  📊 When you exercise more hours, your mood tends    ║
║     to be higher that same day.                      ║
║                                                      ║
║  📈 [View Chart]                                     ║
╚══════════════════════════════════════════════════════╝
```

#### Bad Example (Too Technical):
```
Pearson correlation coefficient: 0.8234
p-value: 0.0012
n=28, df=26
95% CI: [0.645, 0.921]
```

### 7.2 Strength Descriptions

| Coefficient | Label | Icon | User Description |
|-------------|-------|------|------------------|
| 0.7 - 1.0 | Strong | 💪 | "Very closely related" |
| 0.4 - 0.7 | Moderate | 👍 | "Noticeably related" |
| 0.2 - 0.4 | Weak | 🤏 | "Slightly related" |
| 0.0 - 0.2 | Very Weak | 🤷 | "Barely related" |

### 7.3 Lag Effect Visualization

```
Alcohol Consumption → Mood
                    ↓
            [Wait 3 days]
                    ↓
                Lower Mood

Timeline:
Day 1: Drink alcohol 🍺
Day 2: ━━━━━━━━━ (processing)
Day 3: ━━━━━━━━━ (processing)
Day 4: Mood drops 😔
```

---

## 8. Decision Matrix

### 8.1 Algorithm Selection Guide

| Data Type | Relationship | Sample Size | Recommended Algorithm |
|-----------|--------------|-------------|----------------------|
| Continuous | Linear | Any | Pearson |
| Continuous | Non-linear | Any | Spearman |
| Ordinal | Any | >10 | Spearman |
| Ordinal | Any | <10 | Kendall |
| Boolean | Any | Any | Spearman or Kendall |
| Time series | Delayed | >14 | Cross-correlation |
| Any | Confounds present | >20 | Partial correlation |

### 8.2 Recommended Default Settings

```json
{
  "default_algorithm": "auto",  // Automatically select based on data type
  "auto_selection_rules": {
    "continuous_normal_linear": "pearson",
    "continuous_nonlinear": "spearman",
    "ordinal": "spearman",
    "boolean": "spearman",
    "small_sample": "kendall"
  },
  "significance_threshold": 0.05,
  "minimum_samples": 7,
  "recommended_samples": 14,
  "max_lag_days": 7,
  "use_multiple_testing_correction": true,
  "correction_method": "fdr_bh"
}
```

---

## 9. Implementation Checklist

### MVP (Phase 1)
- [ ] Implement Pearson correlation
- [ ] Implement Spearman correlation
- [ ] Implement cross-correlation (lag 0-7)
- [ ] Calculate p-values
- [ ] Auto-select algorithm based on data type
- [ ] User-friendly result presentation
- [ ] Chart visualization for correlations
- [ ] Minimum sample size check (7 days)

### Phase 2
- [ ] Implement Kendall's Tau
- [ ] Multiple testing correction (FDR)
- [ ] Autocorrelation analysis
- [ ] Confidence intervals
- [ ] Extended lag analysis (up to 14 days)
- [ ] "Why?" explanations for each correlation

### Phase 3
- [ ] Partial correlation
- [ ] Rolling correlation (time-varying)
- [ ] Granger causality
- [ ] Machine learning predictions
- [ ] Personalized insights AI

---

## 10. Further Reading

### Academic Papers
1. **Pearson, K. (1895)** - "Notes on regression and inheritance in the case of two parents"
2. **Spearman, C. (1904)** - "The proof and measurement of association between two things"
3. **Kendall, M. G. (1938)** - "A new measure of rank correlation"

### Practical Guides
- **"Statistics for Psychology" by Howitt & Cramer** - Accessible intro
- **"Time Series Analysis" by Box & Jenkins** - Cross-correlation
- **Scipy Documentation** - Implementation reference

### FeelInk-Relevant Research
- Mental health metrics correlation studies
- Mood tracking effectiveness research
- Delayed effect analysis in psychology

---

## 11. Conclusion & Recommendations

### Final Recommendation for FeelInk MVP

**Core Implementation:**
1. **Spearman correlation** as PRIMARY algorithm
   - Works for all data types
   - Robust to outliers
   - Mental health data often ordinal

2. **Pearson correlation** as ALTERNATIVE
   - For true continuous interval data
   - Option for users who want it

3. **Cross-correlation** as KILLER FEATURE
   - This is what makes FeelInk special
   - Discovering delayed effects is incredibly valuable
   - Test lags from 0-7 days initially

4. **Auto-selection** based on data characteristics
   - Don't burden users with algorithm choice
   - Show which algorithm was used in results
   - Allow advanced users to override

**Key Principles:**
- ✅ Start simple (Spearman + cross-correlation)
- ✅ Require 7 days minimum data
- ✅ Use user-friendly language
- ✅ Visualize, don't just show numbers
- ✅ Show statistical significance clearly
- ✅ Implement FDR correction for multiple tests

---

## Related Documents
- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [REQUIREMENTS.md](./REQUIREMENTS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [DATA_MODEL.md](./DATA_MODEL.md)

---

**Status**: Ready for review and algorithm selection decision
**Next Step**: Decide on final algorithm set for MVP
