package com.zhice.platform.controller;

import com.zhice.platform.model.PolicyInput;
import com.zhice.platform.model.ProjectionResponse;
import com.zhice.platform.model.Result;
import com.zhice.platform.service.SimulationService;
import java.util.List;
import java.util.stream.IntStream;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/simulation")
public class SimulationController {
  private final SimulationService simulationService;

  public SimulationController(SimulationService simulationService) {
    this.simulationService = simulationService;
  }

  @PostMapping("/projection")
  public Result<ProjectionResponse> projection(@RequestBody List<PolicyInput> inputs) {
    double baseBirthRate = 1.0;
    List<Double> baseTrend = List.of(1.0, 1.01, 1.02, 1.03, 1.04);
    List<Double> policyTrend = simulationService.calculateProjection(inputs, baseBirthRate);
    List<Integer> years = IntStream.range(0, 5).mapToObj(index -> 2025 + index).toList();
    return Result.success(new ProjectionResponse(years, baseTrend, policyTrend));
  }
}
