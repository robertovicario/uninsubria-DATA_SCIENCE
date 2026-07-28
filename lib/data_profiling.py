# =========================
# Dependencies
# =========================

from pathlib import Path
from ydata_profiling import ProfileReport
import pandas as pd
import webbrowser

# =========================
# Methods
# =========================

def profile_data(
    df: pd.DataFrame,
    out_path: str | Path,
    title: str = 'YData Profiling Report'
) -> None:

    out_path = Path(out_path)
    profile = ProfileReport(
        df, explorative=True, title=title
    )
    profile.to_file(out_path)
    webbrowser.open(
        out_path.resolve().as_uri()
    )

# -------------------------
