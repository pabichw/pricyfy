import React from "react";
import { AxisOptions, Chart } from "react-charts";

export default function ChartArea({ data }: {data: any}) {
  const primaryAxis = React.useMemo<
    AxisOptions<typeof data[number]["data"][number]>
  >(
    () => ({
      getValue: (datum) => datum.primary as Date,
    }),
    []
  );

  const secondaryAxes = React.useMemo<
    AxisOptions<typeof data[number]["data"][number]>[]
  >(
    () => [
      {
        getValue: (datum) => datum.secondary,
        stacked: true,
        // OR
        // elementType: "area",
      },
    ],
    []
  );
  const series = React.useMemo(
    () => ({
      type: "area"
    }),
    []
  );

  return (
    <Chart
      options={{
        data,
        primaryAxis,
        secondaryAxes,
      }}
    />
  );
}
