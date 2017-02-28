package YuzhouLiA1P4;


import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;

public class Graph {
	

	protected List<List<Edge>> adList;
	protected int numN;
	protected int numE;

	public Graph() {
		
		this.adList = new ArrayList<List<Edge>>();
	}

	public Graph(int N) {
		this.numN = N;
		this.adList = new ArrayList<List<Edge>>(N);
		for(int i=0;i<N;i++) {
			this.adList.add(new ArrayList<Edge>());
		}
	}
	
	public int size() {
		return this.numN;
	}
	
	public int computeMST(Tree MST, Graph stmst) {
		HashSet<Integer> selected = new HashSet<Integer>(this.numN);
		selected.add(0);
		PriorityQueue<Edge> edges = new PriorityQueue<Edge>(this.adList.get(0));
		int weight = 0;
		while (selected.size()<this.numN) {
			while (!edges.isEmpty()&&selected.contains(edges.peek().v)) {
				edges.poll();
			}
			Edge e = edges.poll();
			weight += e.weight;
			selected.add(e.v);
			MST.addEdge(e);
			stmst.addEdge(e);
			edges.addAll(this.adList.get(e.v));
		}
		MST.totalWeight = weight;
		return MST.totalWeight;
	} 
	
	public int computeMST(Tree MST) {
		HashSet<Integer> selected = new HashSet<Integer>(this.numN);
		selected.add(0);
		PriorityQueue<Edge> edges = new PriorityQueue<Edge>(this.adList.get(0));
		int weight = 0;
		while (selected.size()<this.numN) {
			while (!edges.isEmpty()&&selected.contains(edges.peek().v)) {
				edges.poll();
			}
			Edge e = edges.poll();
			weight += e.weight;
			selected.add(e.v);
			MST.addEdge(e);	
			edges.addAll(this.adList.get(e.v));
		}
		MST.totalWeight = weight;
		return MST.totalWeight;
	}

	public int recomputeMST(int u,int v,int weight, Tree MST) {
		this.addEdge(u, v, weight);
		/*
		 * Calling another ComputeMST function. This will be much faster because 
		 * the size of the initial graph decreased a lot, and the .extra file usually
		 * only has 1000 changes. 1000 is not a large number so this method will
		 * work fast though is not the fastest.
		 */
		int re = this.computeMST(MST);
		return re;
	}
	public void addEdge(int u, int v, int weight) {
		this.adList.get(u).add(new Edge(u, v, weight));
		this.adList.get(v).add(new Edge(v, u, weight));
	}
	public void addEdge(Edge e) {
		addEdge(e.u, e.v, e.weight);
	}
	public void removeEdge(Edge e) {
		for(int i=0;i<this.adList.get(e.u).size();i++) {
			if(this.adList.get(e.u).get(i).v==e.v) {
				this.adList.get(e.u).remove(i);
				break;
			}
		}
		for(int i=0;i<this.adList.get(e.v).size();i++) {
			if(this.adList.get(e.v).get(i).v==e.v) {
				this.adList.get(e.v).remove(i);
				break;
			}
		}
	}
	public String toString() {
		List<List<String>> s = new ArrayList<List<String>>(this.numN);
		for(int i=0;i<this.numN;i++) {
			s.add(new ArrayList<String>());
			for(int j=0;j<this.adList.get(i).size();j++) {
				s.get(i).add(this.adList.get(i).get(j).toString());
			}
		}
		return s.toString();
	}
}
