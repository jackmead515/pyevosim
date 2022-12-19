
struct Point {
    x: f32,
    y: f32,
}

struct QuadTree {
    root: QuadTreeNode,
}

impl QuadTree {
    pub fn new() -> Self {
        QuadTree {
            root: QuadTreeNode::new(),
        }
    }

    pub fn insert(&mut self, point: Point) {
        self.root.insert(point);
    }

    pub fn get_points(&self) -> Vec<Point> {
        self.root.get_points()
    }

    pub fn get_points_in_range(&self, x: f32, y: f32, radius: f32) -> Vec<Point> {
        let mut points = Vec::new();
        for point in self.get_points() {
            if (point.x - x).powi(2) + (point.y - y).powi(2) < radius.powi(2) {
                points.push(point);
            }
        }
        points
    }
}

struct QuadTreeNode {
    points: Vec<Point>,
    children: Option<[Box<QuadTreeNode>; 4]>,
}

impl QuadTreeNode {
    pub fn new() -> Self {
        QuadTreeNode {
            points: Vec::new(),
            children: None,
        }
    }

    pub fn insert(&mut self, point: Point) {
        if self.children.is_none() {
            self.points.push(point);
            if self.points.len() > 4 {
                self.split();
            }
        } else {
            let children = self.children.as_mut().unwrap();
            let index = self.get_index(point);
            children[index].insert(point);
        }
    }

    pub fn get_points(&self) -> Vec<Point> {
        if self.children.is_none() {
            self.points.clone()
        } else {
            let mut points = Vec::new();
            let children = self.children.as_ref().unwrap();
            for child in children {
                points.append(&mut child.get_points());
            }
            points
        }
    }

    fn split(&mut self) {
        let mut children = [Box::new(QuadTreeNode::new()); 4];
        for point in &self.points {
            let index = self.get_index(*point);
            children[index].insert(*point);
        }
        self.children = Some(children);
        self.points.clear();
    }

    fn get_index(&self, point: Point) -> usize {
        let mut index = 0;
        if point.x > 0.0 {
            index += 1;
        }
        if point.y > 0.0 {
            index += 2;
        }
        index
    }
}

