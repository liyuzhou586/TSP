package YuzhouLiA1P4;

import java.util.ArrayList;
import java.util.List;

class Edge implements Comparable<Edge>{
	int u;
	int v;
	int weight;

	public Edge(int u, int v, int weight) {
		this.u = u;
		this.v = v;
		this.weight = weight;
	}

	public String toString() {
		List<Integer> l = new ArrayList<Integer>();
		l.add(this.u);
		l.add(this.v);
		l.add(this.weight);
		return l.toString();
	}

	@Override public int compareTo(Edge other){
		return this.weight-other.weight;
	}
}
