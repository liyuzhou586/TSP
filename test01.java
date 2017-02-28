package YuzhouLiA1P4;

public class test01 {
	static Graph stmst1 = new Graph(5);
	public static void main(String[] args) {
		Graph g = new Graph(5);
		    g.addEdge(0,1,10);
    		g.addEdge(1,2,10);
		 	g.addEdge(2,3,110);
		    g.addEdge(3,4,30);
		    g.addEdge(2,4,20);
		    g.addEdge(1,4,5);
		    g.addEdge(1,3,8);
		    //Edge ee = new Edge(2,4,1);
		    Edge xx = new Edge(1,4,1000);
		    
		
		Tree MST = new Tree(g.size());
		MST.addEdge(xx);
		System.out.println(g.computeMST(MST,stmst1));
		Tree newmst = new Tree(stmst1.size());
		//System.out.println(stmst1.recomputeMST(1, 0, 1, newmst));
	}
}
