from typing import Annotated

from fastapi import Query

Offset = Annotated[int, Query(ge=0, description="Offset for pagination")]
Limit = Annotated[int, Query(le=1000, description="Limit for pagination")]
Latitude = Annotated[float, Query(ge=-90, le=90, description="Center latitude")]
Longitude = Annotated[float, Query(ge=-180, le=180, description="Center longitude")]
RangeKm = Annotated[float, Query(gt=0, le=500, description="Search radius in kilometers")]
