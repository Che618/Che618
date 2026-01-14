package com.zhice.simulation.model;

/**
 * 政策输入参数。
 */
public class PolicyInput {
    private String name;
    private double value;
    private double elasticity;

    public PolicyInput() {
    }

    public PolicyInput(String name, double value, double elasticity) {
        this.name = name;
        this.value = value;
        this.elasticity = elasticity;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public double getElasticity() {
        return elasticity;
    }

    public void setElasticity(double elasticity) {
        this.elasticity = elasticity;
    }
}
